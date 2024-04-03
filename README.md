# PDF to Speech Converter

This Python script demonstrates how to extract text from a PDF file using the ilovepdf API and then synthesize the
extracted text into speech using Google Cloud Text-to-Speech. The synthesized audio file is then saved to Google Cloud
Storage and downloaded locally.

## Prerequisites

Before running this script, ensure you have the following:

- Python 3 installed on your system.
- Google Cloud project with the Text-to-Speech API enabled.
- Google Cloud Storage bucket created.
- API key for ilovepdf.
- Enable Text-to-Speech on a Google Cloud project.
- Environment variables set for `ILOVEPDF_KEY`, `PROJECT_ID`, and `BUCKET_NAME` containing your ilovepdf API key, Google
  Cloud project ID, and bucket name respectively.

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/jakubswi/PDF-To-Audio.git

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Usage

1. Place the PDF file you want to convert in the `Input` directory.
2. Run the script:
   ```bash
   python pdf_to_speech.py
3. After execution, the synthesized audio file will be saved in the `Output` directory.

## Notes

- The script uses ilovepdf API for PDF extraction, so make sure you have a valid API key and the necessary permissions.
- Ensure that your Google Cloud project has the Text-to-Speech API enabled and that you have set up the necessary
  authentication.
- The script will delete the synthesized audio file from the Google Cloud Storage bucket after downloading it locally.
  Adjust this behavior as needed.

Feel free to contribute by submitting bug reports, feature requests, or pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
