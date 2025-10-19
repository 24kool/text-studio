# Text Studio

A comprehensive text processing platform supporting text transformation, OCR, and multilingual translation.

## Features

- **Text Transformation**: Tone, format, and length adjustment
- **OCR**: Text extraction from images and PDFs
- **Multilingual Translation**: Support for Korean, English, Japanese, and Chinese
- **AI Model Integration**: Gemini API (OpenAI, Claude, etc. to be added in the future)

## Project Structure

```
text-studio/
├── apps/
│   ├── api/                    # FastAPI backend
│   │   ├── src/
│   │   │   ├── main.py        # FastAPI app entry point
│   │   │   ├── routers/       # API routers
│   │   │   ├── services/      # Business logic
│   │   │   ├── models/        # Pydantic models
│   │   │   └── config/        # Configuration management
│   │   ├── .env.example       # Environment variables example
│   │   ├── requirements.txt   # Python dependencies
│   │   └── test.http         # API test file
│   └── web/                   # React frontend (future)
└── README.md
```

## Installation and Setup

### 0. Conda Environment

```bash
conda create -n text-studio python=3.11
conda activate text-studio

### 1. Install Dependencies

```bash
cd apps/api
pip install -r requirements.txt
```

### 2. Environment Configuration

```bash
cp .env.example .env
# Set API keys in the .env file
```

### 3. Run Server

```bash
uvicorn main:app --reload
```

### 4. API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

- `POST /api/v1/transform` - Transform text
- `POST /api/v1/upload-and-transform` - Upload file and transform
- `POST /api/v1/extract-text` - Extract text only from file
- `GET /api/v1/providers` - List available AI providers
- `GET /api/v1/health` - Check service status

## Supported File Formats

- Text: `.txt`
- Images: `.png`, `.jpg`, `.jpeg`, `.webp`
- Documents: `.pdf`

## Environment Variables

```env
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
APP_NAME=Text Studio API
DEBUG=false
MAX_FILE_SIZE=10485760
DEFAULT_AI_PROVIDER=gemini
```
