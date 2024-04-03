import os

import requests
from google.cloud import storage, texttospeech

# Define file paths and names
file_path = "Input/merged.pdf"
file_name_gcloud = "output.wav"

# Google Cloud configuration
location = 'europe-central2'
public_key = os.environ.get("ILOVEPDF_KEY")
project_id = os.environ.get("PROJECT_ID")
bucket_name = os.environ.get("BUCKET_NAME")

# PDF extraction using ilovepdf API
with open(file_path, "rb") as pdf_file:
    # Authenticate and get token from ilovepdf
    token = requests.post("https://api.ilovepdf.com/v1/auth", json={"public_key": public_key}).json()['token']
    header = {"Authorization": f"Bearer {token}"}

    # Start PDF extraction task
    start = requests.get("https://api.ilovepdf.com/v1/start/extract", headers=header).json()
    assigned_server = start['server']
    task_nr = start['task']

    # Upload PDF file
    upload = requests.post(f"https://{assigned_server}/v1/upload", headers=header, data={'task': task_nr},
                           files={"file": pdf_file}).json()
    server_file_name = upload['server_filename']

    # Process PDF extraction
    process = requests.post(f"https://{assigned_server}/v1/process", headers=header,
                            json={"task": task_nr, "tool": "extract",
                                  "files": [
                                      {"server_filename": server_file_name, "filename": file_path.split("/")[-1]}]})

    # Download processed file
    download = requests.get(f"https://{assigned_server}/v1/download/{task_nr}", headers=header)

    # Check if download is successful
    if download.status_code == 200:
        file_content = download.content
        with open('Output/processed_file.txt', 'wb') as f:
            f.write(file_content)
    else:
        print(download.json())

# Read extracted text from processed file
with open("Output/processed_file.txt", "r", encoding='utf-16') as f:
    all_text = f.read()

# Synthesize text to speech using Google Cloud Text-to-Speech
client = texttospeech.TextToSpeechLongAudioSynthesizeClient()
input = texttospeech.SynthesisInput(
    text=all_text
)
audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.LINEAR16)
voice = texttospeech.VoiceSelectionParams(language_code="en-US", name="en-US-Standard-A")
parent = f"projects/{project_id}/locations/{location}"
request = texttospeech.SynthesizeLongAudioRequest(
    parent=parent,
    input=input,
    audio_config=audio_config,
    voice=voice,
    output_gcs_uri=f'gs://{bucket_name}/{file_name_gcloud}',
)

# Perform long audio synthesis request
operation = client.synthesize_long_audio(request=request)
result = operation.result(timeout=300)

# Download synthesized audio from Google Cloud Storage
storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(file_name_gcloud)
blob.download_to_filename(f"Output/{file_name_gcloud}")

# Delete the file from the bucket after download
blob.delete()
