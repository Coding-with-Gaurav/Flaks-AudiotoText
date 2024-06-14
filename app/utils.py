import re
import os
import whisper
import pandas as pd
from pydub import AudioSegment

def extract_information(text):
    text = text.replace("wait", "weight")
    pattern = re.compile(
        r'sample\s*id\s*([a-z\s]*\w+)\s*(?:dash|-)\s*([a-z0-9]+)\s*(?:,|\s+)?\s*weight\s*([\d.]+)', 
        re.IGNORECASE
    )
    matches = pattern.findall(text)

    data = []
    for match in matches:
        sample_id = match[0].strip().upper().replace(" ", "") + "-" + match[1].strip()
        sample_id = sample_id.replace("DASH", "-").replace(",", "").replace(".", "")
        weight = match[2].strip()
        data.append((sample_id, weight))
    return data

def convert_to_wav(mp4_file_path):
    wav_file_path = mp4_file_path.replace(".mp4", ".wav")
    try:
        audio = AudioSegment.from_file(mp4_file_path, format="mp4")
        audio.export(wav_file_path, format="wav")
        print(f"Converted {mp4_file_path} to {wav_file_path}")  # Print success message
        return wav_file_path
    except Exception as e:
        error_message = f"Error converting {mp4_file_path} to WAV: {str(e)}"
        print(error_message)  # Print error message
        return None

def audio_file_to_text(wav_file_path):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(wav_file_path)
        text = result['text']
        print(f"Transcription result: {text}")  # Print success message
        return text
    except Exception as e:
        error_message = f"Error transcribing audio file {wav_file_path}: {str(e)}"
        print(error_message)  # Print error message
        return None

def save_to_excel(data, file_name="sample_file.xlsx"):
    try:
        if data:
            if os.path.exists(file_name):
                df_existing = pd.read_excel(file_name)
                df_new = pd.DataFrame(data, columns=["Sample ID", "Weight"])
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.to_excel(file_name, index=False)
                print(f"Data appended and saved to {file_name}")  # Print success message
            else:
                df = pd.DataFrame(data, columns=["Sample ID", "Weight"])
                df.to_excel(file_name, index=False)
                print(f"New data saved to {file_name}")  # Print success message
        else:
            print("No data to save.")  # Print information message
    except Exception as e:
        error_message = f"Error saving data to {file_name}: {str(e)}"
        print(error_message)  # Print error message

# error during deployment
