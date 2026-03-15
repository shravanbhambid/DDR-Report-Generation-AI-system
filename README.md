# DDR Report Generation AI System

This project is an AI-powered system designed to process a Site Inspection Report and a Thermal Imaging Report, extract the relevant data, and automate the creation of a Detailed Diagnostic Report (DDR).

## Setup Instructions

1. **Install dependencies**. Make sure you have Python installed, then run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your environment variables**.
   Rename `.env.example` to `.env` and insert your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_key_here
   ```

## Usage

You can run the script via the command line by passing the paths to your inspection and thermal report files (either `.txt` or `.pdf`).

```bash
python main.py --inspection "path/to/site_inspection.pdf" --thermal "path/to/thermal_imaging.pdf" --output "output/my_ddr_report.md"
```

### Options:
- `-i, --inspection`: (Required) Path to the Site Inspection report file.
- `-t, --thermal`: (Required) Path to the Thermal Imaging report file.
- `-o, --output`: (Optional) Where to save the generated report. Defaults to `output/DDR_Report.md`.

## Project Structure

- `main.py`: Entry point for the CLI tool.
- `llm_client.py`: Handles interaction with the Google GenAI API, including the retry logic for API limits.
- `pdf_parser.py`: Utility functions for extracting text from PDF wrappers.
- `prompts.py`: The core DDR report template and AI prompt rules.
