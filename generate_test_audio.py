#!/usr/bin/env python3
"""
Generate test audio files for AIscribe using pyttsx3 (offline TTS)

Usage:
    pip install pyttsx3
    python generate_test_audio.py
"""

import pyttsx3
import os

def generate_test_audio():
    """Generate test audio file from doctor-patient conversation"""
    
    print("=" * 60)
    print("AIscribe Test Audio Generator")
    print("=" * 60)
    
    # Initialize TTS engine
    try:
        engine = pyttsx3.init()
    except Exception as e:
        print(f"Error initializing TTS engine: {e}")
        print("\nTroubleshooting:")
        print("- Windows: Should work out of the box")
        print("- Mac: Install using 'brew install espeak'")
        print("- Linux: Install using 'sudo apt-get install espeak'")
        return
    
    # Set properties
    engine.setProperty('rate', 140)  # Speed (words per minute)
    engine.setProperty('volume', 1.0)  # Volume (0.0 to 1.0)
    
    # Get available voices
    voices = engine.getProperty('voices')
    print(f"\nAvailable voices: {len(voices)}")
    
    if len(voices) < 2:
        print("Warning: Less than 2 voices available. Using same voice for both speakers.")
    
    # Test conversations
    conversations = {
        'fever_case': [
            ("Doctor", "Good morning! What brings you in today?"),
            ("Patient", "Hi doctor, I have a fever that started three days ago."),
            ("Doctor", "How high is your fever?"),
            ("Patient", "It's been around one hundred and two degrees Fahrenheit."),
            ("Doctor", "Any other symptoms?"),
            ("Patient", "Yes, I have body aches and a runny nose."),
            ("Doctor", "Based on your symptoms, you have a severe fever with mild cold symptoms. I'll prescribe Doro 150, Cyprosine, Indolo 160, and Citrogen."),
            ("Patient", "Thank you, doctor. When should I take these?"),
            ("Doctor", "Take Doro 150 twice daily. If your fever persists beyond three days, please come back for a follow-up."),
            ("Patient", "Okay, I will. Thank you so much."),
        ],
        'respiratory_issue': [
            ("Doctor", "Hello, what seems to be the problem today?"),
            ("Patient", "I've been having trouble breathing and a persistent cough."),
            ("Doctor", "How long has this been going on?"),
            ("Patient", "About a week now. The cough is producing yellow mucus."),
            ("Doctor", "Any fever or chest pain?"),
            ("Patient", "A low-grade fever around one hundred degrees, and some chest tightness."),
            ("Doctor", "I hear some wheezing in your lungs. This could be bronchitis. I'll prescribe an antibiotic and an inhaler."),
            ("Patient", "What should I do besides taking the medication?"),
            ("Doctor", "Get plenty of rest, drink lots of fluids, and avoid strenuous activities."),
            ("Patient", "Thank you, doctor."),
        ],
        'simple_consultation': [
            ("Doctor", "Good afternoon. How can I help you today?"),
            ("Patient", "I've had a headache for two days."),
            ("Doctor", "Can you describe the pain?"),
            ("Patient", "It's a throbbing pain on both sides of my head."),
            ("Doctor", "Any nausea or sensitivity to light?"),
            ("Patient", "A little nausea, yes."),
            ("Doctor", "This sounds like a tension headache. I'll recommend ibuprofen and rest."),
            ("Patient", "Should I be worried?"),
            ("Doctor", "No, but if it persists or gets worse, come back to see me."),
            ("Patient", "Thank you, doctor."),
        ]
    }
    
    # Create test_audio directory
    os.makedirs('test_audio', exist_ok=True)
    
    # Generate audio files for each conversation
    for conv_name, dialogue in conversations.items():
        print(f"\n{'='*60}")
        print(f"Generating: {conv_name}.mp3")
        print(f"{'='*60}")
        
        # Create full conversation text
        full_text = ""
        
        for i, (speaker, text) in enumerate(dialogue):
            # Alternate between voices
            if len(voices) >= 2:
                if speaker == "Doctor":
                    engine.setProperty('voice', voices[0].id)  # First voice
                else:
                    engine.setProperty('voice', voices[1].id)  # Second voice
            
            # Add pauses between speakers
            if i > 0:
                full_text += " ... "
            
            full_text += text
            print(f"  {speaker}: {text}")
        
        # Save to file
        output_file = os.path.join('test_audio', f'{conv_name}.mp3')
        
        try:
            engine.save_to_file(full_text, output_file)
            engine.runAndWait()
            print(f"\n✓ Created: {output_file}")
        except Exception as e:
            print(f"\n✗ Error creating {output_file}: {e}")
    
    print("\n" + "="*60)
    print("Test audio generation complete!")
    print("="*60)
    print(f"\nFiles saved in: {os.path.abspath('test_audio')}/")
    print("\nNext steps:")
    print("1. Open AIscribe: http://localhost:5000")
    print("2. Upload any of the generated MP3 files")
    print("3. Click 'Process Audio'")
    print("4. View the results!")
    print("\nNote: Voice quality depends on your system's TTS engine.")
    print("For better quality, use online TTS services (see TEST_AUDIO_SOURCES.md)")

if __name__ == "__main__":
    generate_test_audio()



