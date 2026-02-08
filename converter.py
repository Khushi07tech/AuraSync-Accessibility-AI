import re

# This is the text I got from the Build Tab
raw_text = """00:00:00 - 00:00:03
Three young men stand on a lawn, one wearing a banana costume. A large blue ball is thrown directly at the camera, knocking it over.
00:00:03 - 00:00:05
A man in a banana costume throws a red ball at a stack of buckets, but hits the camera instead.
00:00:05 - 00:00:08
An indoor trick shot attempt with a ball results in the ball hitting the recording device.
00:00:08 - 00:00:12
Three men in a room with tables and buckets try a trick shot with a soccer ball, which ends up hitting the camera."""


def text_to_srt(text):
    # 1. Clean up the text: split into lines and remove empty ones
    lines = [line.strip() for line in text.strip().split('\n') if line.strip()]

    srt_output = ""
    counter = 1

    # 2. Safety Check: We need pairs (Timestamp + Description)
    for i in range(0, len(lines) - 1, 2):
        timestamp_part = lines[i]
        description = lines[i + 1]

        # Check if the line actually looks like a timestamp (contains ' - ')
        if ' - ' in timestamp_part:
            try:
                times = timestamp_part.split(' - ')
                # Formatting for SRT (adding the ,000 milliseconds)
                start = times[0].strip() + ",000"
                end = times[1].strip() + ",000"

                # Build the SRT block
                srt_output += f"{counter}\n"
                srt_output += f"{start.replace('.', ',')} --> {end.replace('.', ',')}\n"
                srt_output += f"{description}\n\n"
                counter += 1
            except Exception:
                continue  # Skip lines that don't match the format

    return srt_output

# Generate and save
srt_content = text_to_srt(raw_text)
with open("accessibility_narration.srt", "w") as f:
    f.write(srt_content)

print("🚀 Success! 'accessibility_narration.srt' has been created.")