import time, re, io
from google import genai
from google.genai import types
from gtts import gTTS


def process_video_ai(video_path, mode, level_choice, api_key):
    # We initialize the client INSIDE the function using the key from the UI
    client = genai.Client(api_key=api_key)

    myfile = client.files.upload(file=video_path, config={'mime_type': 'video/mp4'})
    while myfile.state.name == "PROCESSING":
        time.sleep(1)
        myfile = client.files.get(name=myfile.name)

    if mode == "Visually Impaired":
        prompt = """
        ACT AS: A professional Cinematic Audio Describer for the blind.
        STRICT OUTPUT RULE: Start your response immediately with the first timestamp. 
        FORMAT: HH:MM:SS - HH:MM:SS -> [Vivid description of visual action]
        CONTENT: Capture micro-expressions, gestures, and the 'vibe' of the scene. Use natural language.
        """
    else:
        prompt = """
        ACT AS: An Expert Accessibility Specialist for the Deaf.
        STRICT OUTPUT RULE: Start your response immediately with the first timestamp. 
        FORMAT: HH:MM:SS - HH:MM:SS -> [Dialogue or Environmental Context]
        CONTENT: Describe the SOURCE of sounds. Transcribe dialogue. Use concrete nouns.
        """

    if level_choice == "Instant":
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[myfile, prompt]
        )
        thoughts = "Thinking was disabled for Instant Mode."
    else:
        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(
                include_thoughts=True,
            )
        )
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=[myfile, prompt],
            config=config
        )
        thoughts = "".join(part.thought for part in response.candidates[0].content.parts if part.thought)

    narration = "".join(part.text for part in response.candidates[0].content.parts if not part.thought)
    return narration, thoughts


def generate_natural_audio(narration):
    clean_text = re.sub(r'\d{2}:\d{2}:\d{2} - \d{2}:\d{2}:\d{2}', '', narration)
    clean_text = clean_text.replace('->', '').replace('*', '').strip()
    if not clean_text: clean_text = "Analysis complete."
    tts = gTTS(text=clean_text, lang='en', slow=False)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    return audio_fp.getvalue()