import pytesseract
from PIL import Image
import fitz  # PyMuPDF
from typing import Union
import io
import os
from pathlib import Path


class OCRService:
    """OCR service - Extract text from images and PDFs"""
    
    def __init__(self):
        # Tesseract configuration (for macOS)
        if os.path.exists('/opt/homebrew/bin/tesseract'):
            pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
        elif os.path.exists('/usr/local/bin/tesseract'):
            pytesseract.pytesseract.tesseract_cmd = '/usr/local/bin/tesseract'
    
    async def extract_text_from_image(self, image_data: bytes) -> str:
        """Extract text from image."""
        try:
            # Convert byte data to PIL Image
            image = Image.open(io.BytesIO(image_data))
            
            # Perform OCR (Korean + English)
            text = pytesseract.image_to_string(
                image, 
                lang='kor+eng',
                config='--oem 3 --psm 6'
            )
            
            return text.strip()
        
        except Exception as e:
            raise Exception(f"Error during image OCR processing: {str(e)}")
    
    async def extract_text_from_pdf(self, pdf_data: bytes) -> str:
        """Extract text from PDF."""
        try:
            # Open PDF document
            pdf_document = fitz.open(stream=pdf_data, filetype="pdf")
            
            extracted_text = []
            
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                
                # Try to extract text
                text = page.get_text()
                
                if text.strip():
                    # Add text if available
                    extracted_text.append(text)
                else:
                    # If no text, convert to image and perform OCR
                    pix = page.get_pixmap()
                    img_data = pix.tobytes("png")
                    ocr_text = await self.extract_text_from_image(img_data)
                    if ocr_text.strip():
                        extracted_text.append(ocr_text)
            
            pdf_document.close()
            
            return "\n\n".join(extracted_text).strip()
        
        except Exception as e:
            raise Exception(f"Error during PDF processing: {str(e)}")
    
    async def extract_text_from_file(self, file_data: bytes, filename: str) -> str:
        """Select appropriate text extraction method based on file extension."""
        
        file_extension = Path(filename).suffix.lower()
        
        if file_extension == '.pdf':
            return await self.extract_text_from_pdf(file_data)
        
        elif file_extension in ['.png', '.jpg', '.jpeg', '.webp', '.bmp', '.tiff']:
            return await self.extract_text_from_image(file_data)
        
        elif file_extension == '.txt':
            # Read text file directly
            try:
                return file_data.decode('utf-8')
            except UnicodeDecodeError:
                # Try other encodings if UTF-8 fails
                try:
                    return file_data.decode('cp949')  # Korean Windows encoding
                except UnicodeDecodeError:
                    return file_data.decode('latin-1')  # Last attempt
        
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")


# Singleton instance
ocr_service = OCRService()
