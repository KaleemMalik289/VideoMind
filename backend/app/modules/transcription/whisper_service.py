class WhisperService:
    """Stub for the Whisper audio transcription module."""
    
    def __init__(self):
        # self.model = load_faster_whisper()
        pass
        
    def transcribe(self, audio_path: str) -> dict:
        """Transcribes audio and returns timestamps."""
        # result = self.model.transcribe(audio_path)
        # return result
        return {"text": "Stub transcript", "segments": []}
