import json
from loguru import logger
from typing import Tuple
from app.core.settings import settings
from app.modules.timeline.schemas import TimelineEntry
from app.modules.timeline.synchronizer import TimelineSynchronizer
from app.modules.timeline.deduplicator import TextDeduplicator

class TimelineBuilder:
    """Merges OCR and Transcript datasets into a sequential Timeline."""
    
    @staticmethod
    def _parse_time(ts_str: str) -> float:
        """Converts HH:MM:SS.mmm to seconds"""
        try:
            parts = ts_str.split(':')
            if len(parts) == 3:
                h, m, s = parts
                return int(h) * 3600 + int(m) * 60 + float(s)
            elif len(parts) == 2:
                m, s = parts
                return int(m) * 60 + float(s)
            return float(ts_str)
        except Exception:
            return 0.0

    @staticmethod
    def build(ocr_frames: list, transcript_segments: list) -> Tuple[list[TimelineEntry], int, int]:
        """
        Iterates over transcript segments as the primary anchor, and attaches nearby OCR.
        Then iterates over orphaned OCR frames and injects them.
        Returns the sorted entries, plus merge stats.
        """
        entries = []
        timeline_id = 1
        
        ocr_merged_count = 0
        transcript_merged_count = len(transcript_segments)
        
        # We will keep track of which OCR frames have been matched
        matched_ocr_indices = set()
        
        # 1. Primary pass: Transcripts
        for t_seg in transcript_segments:
            start = t_seg.get("start", 0.0)
            end = t_seg.get("end", 0.0)
            text = t_seg.get("text", "")
            
            # Find all OCR frames that synchronize to this transcript
            associated_ocrs = []
            frame_id = None
            frame_path = None
            
            for i, ocr in enumerate(ocr_frames):
                if i in matched_ocr_indices:
                    continue
                    
                ocr_time = TimelineBuilder._parse_time(ocr.get("timestamp", "0.0"))
                nearest = TimelineSynchronizer.find_nearest_segment(ocr_time, transcript_segments)
                
                if nearest and nearest.get("segment_id") == t_seg.get("segment_id"):
                    # Attach this OCR
                    ocr_text_list = [d.get("text") for d in ocr.get("detections", [])]
                    full_ocr_text = "\n".join(ocr_text_list)
                    
                    if full_ocr_text.strip():
                        associated_ocrs.append(full_ocr_text)
                    
                    if frame_id is None:
                        frame_id = ocr.get("frame_id")
                        frame_path = ocr.get("image")
                        
                    matched_ocr_indices.add(i)
                    ocr_merged_count += 1
            
            # Deduplicate OCRs within this single segment
            deduped_ocrs = []
            if associated_ocrs:
                if settings.REMOVE_DUPLICATE_OCR:
                    last_ocr = ""
                    for o in associated_ocrs:
                        if not TextDeduplicator.is_duplicate(last_ocr, o):
                            deduped_ocrs.append(o)
                            last_ocr = o
                else:
                    deduped_ocrs = associated_ocrs

            entries.append(TimelineEntry(
                timeline_id=timeline_id,
                start=start,
                end=end,
                transcript=text,
                ocr_text=deduped_ocrs,
                frame_id=frame_id,
                frame_path=frame_path
            ))
            timeline_id += 1
            
        # 2. Secondary pass: Orphaned OCR frames
        for i, ocr in enumerate(ocr_frames):
            if i in matched_ocr_indices:
                continue
                
            ocr_time = TimelineBuilder._parse_time(ocr.get("timestamp", "0.0"))
            ocr_text_list = [d.get("text") for d in ocr.get("detections", [])]
            full_ocr_text = "\n".join(ocr_text_list)
            
            if not full_ocr_text.strip():
                continue
                
            entries.append(TimelineEntry(
                timeline_id=0,
                start=ocr_time,
                end=ocr_time + 1.0,
                transcript=None,
                ocr_text=[full_ocr_text],
                frame_id=ocr.get("frame_id"),
                frame_path=ocr.get("image")
            ))
            ocr_merged_count += 1
            
        # 3. Sort completely chronologically
        entries.sort(key=lambda x: x.start)
        
        # 4. Global Deduplication across consecutive entries
        final_entries = []
        last_transcript = ""
        last_ocr_joined = ""
        
        for idx, entry in enumerate(entries):
            entry.timeline_id = idx + 1
            
            current_ocr_joined = "\n".join(entry.ocr_text)
            
            if settings.REMOVE_DUPLICATE_TRANSCRIPT and entry.transcript:
                if TextDeduplicator.deduplicate_transcript(last_transcript, entry.transcript):
                    entry.transcript = None
                else:
                    last_transcript = entry.transcript
                    
            if settings.REMOVE_DUPLICATE_OCR and current_ocr_joined:
                if TextDeduplicator.is_duplicate(last_ocr_joined, current_ocr_joined):
                    entry.ocr_text = []
                else:
                    last_ocr_joined = current_ocr_joined
                    
            final_entries.append(entry)
            
        return final_entries, ocr_merged_count, transcript_merged_count
