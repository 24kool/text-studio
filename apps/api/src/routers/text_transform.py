from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import Optional
import os
from pathlib import Path

from ..models.schemas import (
    TextTransformRequest, TextTransformResponse, FileUploadResponse, 
    ErrorResponse, AIProvider, TransformationType, ToneOption, 
    FormatOption, LengthOption, LanguageOption
)
from ..services.ai_service import ai_service
# from ..services.ocr_service import ocr_service  # TODO: OCR feature will be added later
from ..config.settings import settings

router = APIRouter(prefix="/api/v1", tags=["text-transform"])


@router.post("/transform", response_model=TextTransformResponse)
async def transform_text(request: TextTransformRequest):
    """Transform text."""
    
    try:
        transformed_text = await ai_service.transform_text(
            text=request.text,
            transformation_type=request.transformation_type,
            provider=request.ai_provider,
            tone=request.tone,
            format=request.format,
            length=request.length,
            target_language=request.target_language,
            custom_instruction=request.custom_instruction
        )
        
        return TextTransformResponse(
            original_text=request.text,
            transformed_text=transformed_text,
            transformation_type=request.transformation_type,
            ai_provider=request.ai_provider,
            success=True
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# TODO: OCR feature will be added later
# @router.post("/upload-and-transform", response_model=TextTransformResponse)
# async def upload_and_transform(
#     file: UploadFile = File(...),
#     transformation_type: TransformationType = Form(...),
#     ai_provider: AIProvider = Form(AIProvider.GEMINI),
#     tone: Optional[ToneOption] = Form(None),
#     format: Optional[FormatOption] = Form(None),
#     length: Optional[LengthOption] = Form(None),
#     target_language: Optional[LanguageOption] = Form(None),
#     custom_instruction: Optional[str] = Form(None)
# ):
#     """Upload file, extract text, and transform it."""
#     
#     # Validate file size
#     if file.size > settings.max_file_size:
#         raise HTTPException(
#             status_code=413, 
#             detail=f"File size too large. Maximum {settings.max_file_size // (1024*1024)}MB allowed."
#         )
#     
#     # Validate file extension
#     file_extension = Path(file.filename).suffix.lower()
#     if file_extension not in settings.allowed_file_types:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Unsupported file format. Allowed formats: {', '.join(settings.allowed_file_types)}"
#         )
#     
#     try:
#         # Read file data
#         file_data = await file.read()
#         
#         # Extract text using OCR
#         extracted_text = await ocr_service.extract_text_from_file(file_data, file.filename)
#         
#         if not extracted_text.strip():
#             raise HTTPException(status_code=400, detail="Could not extract text from file.")
#         
#         # Transform text
#         transformed_text = await ai_service.transform_text(
#             text=extracted_text,
#             transformation_type=transformation_type,
#             provider=ai_provider,
#             tone=tone,
#             format=format,
#             length=length,
#             target_language=target_language,
#             custom_instruction=custom_instruction
#         )
#         
#         return TextTransformResponse(
#             original_text=extracted_text,
#             transformed_text=transformed_text,
#             transformation_type=transformation_type,
#             ai_provider=ai_provider,
#             success=True
#         )
#     
#     except HTTPException:
#         raise
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


# OCR 기능 추가 후 활성화 예정
# @router.post("/extract-text", response_model=FileUploadResponse)
# async def extract_text_from_file(file: UploadFile = File(...)):
#     """Extract text only from file."""
#     
#     # Validate file size
#     if file.size > settings.max_file_size:
#         raise HTTPException(
#             status_code=413, 
#             detail=f"File size too large. Maximum {settings.max_file_size // (1024*1024)}MB allowed."
#         )
#     
#     # Validate file extension
#     file_extension = Path(file.filename).suffix.lower()
#     if file_extension not in settings.allowed_file_types:
#         raise HTTPException(
#             status_code=400,
#             detail=f"Unsupported file format. Allowed formats: {', '.join(settings.allowed_file_types)}"
#         )
#     
#     try:
#         # Read file data
#         file_data = await file.read()
#         
#         # Extract text using OCR
#         extracted_text = await ocr_service.extract_text_from_file(file_data, file.filename)
#         
#         return FileUploadResponse(
#             filename=file.filename,
#             file_size=file.size,
#             extracted_text=extracted_text,
#             message="Text extraction completed."
#         )
#     
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")


@router.get("/providers")
async def get_available_providers():
    """Return list of available AI providers."""
    
    try:
        providers = ai_service.get_available_providers()
        return {
            "available_providers": [provider.value for provider in providers],
            "default_provider": settings.default_ai_provider
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health")
async def health_check():
    """Check API status."""
    
    available_providers = ai_service.get_available_providers()
    
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "available_providers": len(available_providers),
        "providers": [provider.value for provider in available_providers]
    }
