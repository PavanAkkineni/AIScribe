"""AssemblyAI transcription service with speaker diarization"""

import assemblyai as aai
import time
from logger_config import setup_logger
from config import ASSEMBLYAI_API_KEY

logger = setup_logger()

class TranscriptionService:
    """Handle audio transcription with speaker diarization using AssemblyAI"""
    
    def __init__(self):
        aai.settings.api_key = ASSEMBLYAI_API_KEY
        logger.info("✓ TranscriptionService initialized with AssemblyAI")
    
    def transcribe_audio(self, audio_file_path, enable_diarization=True):
        """
        Transcribe audio file with optional speaker diarization
        
        Args:
            audio_file_path: Path to the audio file
            enable_diarization: Whether to enable speaker diarization (default: True)
            
        Returns:
            dict: Contains transcript, speaker-labeled dialogue (if diarization enabled), and metadata
        """
        try:
            logger.info(f"📤 Uploading audio file: {audio_file_path}")
            
            # Configure transcription
            if enable_diarization:
                logger.info("🎙️ Starting transcription with speaker diarization...")
                config = aai.TranscriptionConfig(
                    speaker_labels=True,
                    speakers_expected=2  # Doctor and Patient
                )
            else:
                logger.info("📝 Starting transcription without speaker diarization (notes mode)...")
                config = aai.TranscriptionConfig(
                    speaker_labels=False
                )
            
            transcriber = aai.Transcriber()
            transcript = transcriber.transcribe(audio_file_path, config=config)
            
            # Wait for transcription to complete
            while transcript.status not in [aai.TranscriptStatus.completed, aai.TranscriptStatus.error]:
                logger.info("⏳ Transcription in progress...")
                time.sleep(3)
                transcript = transcriber.get_transcript(transcript.id)
            
            if transcript.status == aai.TranscriptStatus.error:
                logger.error(f"❌ Transcription failed: {transcript.error}")
                return {
                    'success': False,
                    'error': transcript.error
                }
            
            logger.info("✓ Transcription completed successfully")
            
            # Format the dialogue
            if enable_diarization:
                # Format with speaker labels
                dialogue = self._format_dialogue(transcript)
                logger.info(f"📝 Generated dialogue with {len(dialogue)} exchanges")
            else:
                # For summary notes, create a single entry with the full text
                dialogue = [{
                    'speaker': 'Doctor Notes',
                    'text': transcript.text,
                    'confidence': transcript.confidence if hasattr(transcript, 'confidence') else None
                }]
                logger.info(f"📝 Generated summary notes ({len(transcript.text)} characters)")
            
            return {
                'success': True,
                'full_text': transcript.text,
                'dialogue': dialogue,
                'confidence': transcript.confidence if hasattr(transcript, 'confidence') else None,
                'duration': transcript.audio_duration if hasattr(transcript, 'audio_duration') else None,
                'is_diarized': enable_diarization
            }
            
        except Exception as e:
            logger.error(f"❌ Error during transcription: {str(e)}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def _format_dialogue(self, transcript):
        """
        Format the transcript into speaker-labeled dialogue
        
        Args:
            transcript: AssemblyAI transcript object
            
        Returns:
            list: List of dialogue entries with speaker and text
        """
        dialogue = []
        
        if not transcript.utterances:
            logger.warning("⚠️ No utterances found in transcript")
            return dialogue
        
        # Map speakers to roles (A = Doctor, B = Patient by default)
        speaker_map = {}
        
        for utterance in transcript.utterances:
            speaker_id = utterance.speaker
            
            # Assign roles based on speaker ID
            if speaker_id not in speaker_map:
                if len(speaker_map) == 0:
                    speaker_map[speaker_id] = "Doctor"
                else:
                    speaker_map[speaker_id] = "Patient"
            
            role = speaker_map[speaker_id]
            
            dialogue.append({
                'speaker': role,
                'text': utterance.text,
                'confidence': utterance.confidence if hasattr(utterance, 'confidence') else None
            })
        
        logger.info(f"👥 Identified {len(speaker_map)} speakers")
        
        return dialogue
    
    def format_dialogue_text(self, dialogue):
        """
        Convert dialogue list to formatted text
        
        Args:
            dialogue: List of dialogue entries
            
        Returns:
            str: Formatted dialogue text
        """
        formatted_lines = []
        
        for entry in dialogue:
            speaker = entry['speaker'].lower()
            text = entry['text']
            formatted_lines.append(f"{speaker}: {text}")
        
        return "\n".join(formatted_lines)

