from loguru import logger
from app.core.settings import settings
from app.modules.chunking.schemas import SemanticChunk
from app.modules.chunking.chunker import SemanticChunker
from app.modules.chunking.overlap import OverlapManager

class ChunkBuilder:
    """Builds semantic chunks by walking the timeline and grouping context."""
    
    @staticmethod
    def build(timeline_entries: list) -> list[SemanticChunk]:
        chunks = []
        current_chunk_entries = []
        current_tokens = 0
        chunk_id = 1
        
        max_tokens = settings.MAX_CHUNK_TOKENS
        min_tokens = settings.MIN_CHUNK_TOKENS
        
        i = 0
        while i < len(timeline_entries):
            entry = timeline_entries[i]
            entry_tokens = SemanticChunker.estimate_entry_tokens(entry)
            
            # If a single entry is massive, we must add it and slice immediately after
            if entry_tokens >= max_tokens:
                if current_chunk_entries:
                    chunks.append(ChunkBuilder._create_chunk(chunk_id, current_chunk_entries, current_tokens))
                    chunk_id += 1
                    current_chunk_entries = []
                    current_tokens = 0
                
                chunks.append(ChunkBuilder._create_chunk(chunk_id, [entry], entry_tokens))
                chunk_id += 1
                i += 1
                
                # Apply overlap if needed
                if settings.ENABLE_CONTEXT_OVERLAP and i < len(timeline_entries):
                    overlap = OverlapManager.get_overlap_entries([entry], entry.get("end", 0.0))
                    current_chunk_entries.extend(overlap)
                    current_tokens = sum(SemanticChunker.estimate_entry_tokens(e) for e in overlap)
                continue
                
            # If adding this entry pushes us over MAX, we slice the current chunk BEFORE adding it
            if current_tokens + entry_tokens > max_tokens:
                chunks.append(ChunkBuilder._create_chunk(chunk_id, current_chunk_entries, current_tokens))
                chunk_id += 1
                
                # Apply overlap from the chunk we just closed
                if settings.ENABLE_CONTEXT_OVERLAP:
                    last_end = current_chunk_entries[-1].get("end", 0.0) if current_chunk_entries else 0.0
                    overlap = OverlapManager.get_overlap_entries(current_chunk_entries, last_end)
                    current_chunk_entries = overlap
                    current_tokens = sum(SemanticChunker.estimate_entry_tokens(e) for e in overlap)
                else:
                    current_chunk_entries = []
                    current_tokens = 0
                    
            # Add entry to current chunk
            current_chunk_entries.append(entry)
            current_tokens += entry_tokens
            i += 1
            
            # If we hit MIN, check for a semantic break (e.g. gap > 1 second between entries)
            if current_tokens >= min_tokens and i < len(timeline_entries):
                next_entry = timeline_entries[i]
                gap = next_entry.get("start", 0.0) - entry.get("end", 0.0)
                if gap > 1.0:
                    chunks.append(ChunkBuilder._create_chunk(chunk_id, current_chunk_entries, current_tokens))
                    chunk_id += 1
                    
                    if settings.ENABLE_CONTEXT_OVERLAP:
                        last_end = current_chunk_entries[-1].get("end", 0.0)
                        overlap = OverlapManager.get_overlap_entries(current_chunk_entries, last_end)
                        current_chunk_entries = overlap
                        current_tokens = sum(SemanticChunker.estimate_entry_tokens(e) for e in overlap)
                    else:
                        current_chunk_entries = []
                        current_tokens = 0
                        
        # Add remaining entries
        if current_chunk_entries:
            # Prevent creating an empty trailing chunk if it only contains carry-over overlap
            if len(chunks) == 0 or current_chunk_entries != OverlapManager.get_overlap_entries(current_chunk_entries, current_chunk_entries[-1].get("end", 0.0)):
                chunks.append(ChunkBuilder._create_chunk(chunk_id, current_chunk_entries, current_tokens))
            
        return [c for c in chunks if c is not None]

    @staticmethod
    def _create_chunk(chunk_id: int, entries: list, tokens: int) -> SemanticChunk:
        if not entries:
            return None
            
        start = entries[0].get("start", 0.0)
        end = entries[-1].get("end", 0.0)
        
        transcripts = []
        ocr_texts = []
        frames = []
        
        for e in entries:
            if e.get("transcript"):
                transcripts.append(e["transcript"])
            if e.get("ocr_text"):
                ocr_texts.extend(e["ocr_text"])
            if e.get("frame_id") is not None:
                frames.append(e["frame_id"])
                
        deduped_ocr = []
        last_ocr = None
        for txt in ocr_texts:
            if txt != last_ocr:
                deduped_ocr.append(txt)
                last_ocr = txt
                
        deduped_frames = list(dict.fromkeys(frames))
        
        return SemanticChunk(
            chunk_id=chunk_id,
            start=round(start, 2),
            end=round(end, 2),
            transcript=" ".join(transcripts),
            ocr_text=deduped_ocr,
            frames=deduped_frames,
            estimated_tokens=tokens
        )
