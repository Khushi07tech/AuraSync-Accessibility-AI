import time, re, io
from google import genai
from google.genai import types
from gtts import gTTS

API_KEY = "YOUR_API_KEY_GOES_HERE"
client = genai.Client(api_key=API_KEY)

def process_video_ai(video_path, mode, level_choice):
    myfile = client.files.upload(file=video_path, config={'mime_type': 'video/mp4'})
    while myfile.state.name == "PROCESSING":
        time.sleep(1)
        myfile = client.files.get(name=myfile.name)

    # Context-aware prompts
        # Context-aware prompts with strict formatting
        if mode == "Visually Impaired":
            prompt = """
            ACT AS: A professional Cinematic Audio Describer for the blind.

            STRICT OUTPUT RULE: Start your response immediately with the first timestamp. 
            Do NOT say "Sure," "Here is," or "Okay." Output ONLY the data.

            FORMAT:
            HH:MM:SS - HH:MM:SS -> [Vivid description of visual action]

            CONTENT:
            1. Capture micro-expressions, gestures, and the 'vibe' of the scene.
            2. Descriptions must be cohesive and flow naturally.
            3. Never say 'The video shows'—just describe the world.
            4. Use a human, natural and cohesive language.
            """
        else:
            prompt = """
            ACT AS: An Expert Accessibility Specialist for the Deaf.

            STRICT OUTPUT RULE: Start your response immediately with the first timestamp. 
            Do NOT say "Sure," "I've generated," or provide any intro/outro. Output ONLY the data.

            FORMAT:
            HH:MM:SS - HH:MM:SS -> [Dialogue or Environmental Context]

            CONTENT:
            1. DO NOT just list sounds. Describe the SOURCE (e.g., [The wooden chair leg snaps]).
            2. Transcribe spoken dialogue with 100% accuracy.
            3. Include emotional cues in brackets (e.g., [Sarcastic tone], [Whispering]).
            4. Use a human, natural and cohesive language.
            5. Use clear, concrete nouns and active verbs. Avoid complex metaphors that rely on sound-puns.
            """
    # DYNAMIC CONFIGURATION
    if level_choice == "Instant":
        # Lightning fast - skips the reasoning process entirely
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[myfile, prompt]
        )
        thoughts = "Thinking was disabled for Instant Mode."
    else:
        # User selected a specific depth (Low, Medium, or High)
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
                thinking_level=level_choice.upper() # Converts 'Low' to 'LOW'
            )
        )
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[myfile, prompt],
            config=config
        )
        thoughts = "".join(part.text for part in response.candidates[0].content.parts if part.thought)

    narration = "".join(part.text for part in response.candidates[0].content.parts if not part.thought)
    return narration, thoughts

def generate_natural_audio(narration):
    clean_text = re.sub(r'\d{2}:\d{2}:\d{2} - \d{2}:\d{2}:\d{2}', '', narration)
    clean_text = clean_text.replace('->', '').replace('*', '').strip()
    tts = gTTS(text=clean_text, lang='en', slow=False)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    return audio_fp.getvalue()