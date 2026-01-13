# File Text Extraction API

A Django-based API that scans a directory containing files of multiple formats (PDF, DOCX, XLSX, TXT) and extracts clean, readable text from each file into a JSON output.

## Features

- **Multi-format Support**: Extracts text from `.pdf`, `.docx`, `.xlsx`, and `.txt` files.
- **Text Cleaning**: Normalizes unicode and removes non-printable characters.
- **REST API**: Simple endpoints to trigger extraction and retrieve results.
- **JSON Output**: structured output with file names and extracted contents.

## Setup Instructions

### Prerequisites
- Python 3.8+

### Installation

1. Clone the repository (or navigate to the project directory).
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run migrations (not strictly necessary as we don't use DB models, but good practice):
   ```bash
   python manage.py migrate
   ```

## Usage

1. **Start the Server**:
   ```bash
   python manage.py runserver
   ```

2. **Trigger Extraction (POST)**:
   Send a POST request to `/extract-text/` with the absolute path to the directory you want to scan.
   ```bash
   curl -X POST -H "Content-Type: application/json" \
     -d '{"directory_path": "/absolute/path/to/files"}' \
     http://127.0.0.1:8000/extract-text/
   ```

3. **Get Results (GET)**:
   Retrieve the content of the generated `output.json` file.
   ```bash
   curl -X GET http://127.0.0.1:8000/extract-text/
   ```

## Text Cleaning Approach

The text cleaning logic is implemented in `api/utils.py` and performs the following:
1. **Unicode Normalization**: Uses `unicodedata.normalize('NFKC', text)` to standardize characters.
2. **Filtering**: Removes non-printable characters while preserving standard whitespace (newlines, tabs).
3. **Trimming**: Removes leading/trailing whitespace.

## API Reference

### `POST /extract-text/`
- **Body**: `{"directory_path": "/path/to/files"}`
- **Response**: `{"message": "Successfully processed N files...", "output_file": "output.json"}`

### `GET /extract-text/`
- **Response**: JSON array of extracted contents.
  ```json
  [
    {
      "file": "example.pdf",
      "contents": "Extracted text..."
    }
  ]
  ```
