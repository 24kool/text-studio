from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from enum import Enum


class TransformationType(str, Enum):
    TONE = "tone"
    FORMAT = "format"
    LENGTH = "length"
    LANGUAGE = "language"


class ToneOption(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    FRIENDLY = "friendly"
    PROFESSIONAL = "professional"
    POLITE = "polite"


class FormatOption(str, Enum):
    EMAIL = "email"
    REPORT = "report"
    SNS = "sns"
    BLOG = "blog"
    SUMMARY = "summary"


class LengthOption(str, Enum):
    EXPAND = "expand"
    SUMMARIZE = "summarize"
    MAINTAIN = "maintain"


class LanguageOption(str, Enum):
    KOREAN = "ko"
    ENGLISH = "en"
    JAPANESE = "ja"
    CHINESE = "zh"


class AIProvider(str, Enum):
    GEMINI = "gemini"
    OPENAI = "openai"


class TextTransformRequest(BaseModel):
    text: str = Field(..., description="Text to transform")
    transformation_type: TransformationType = Field(..., description="Type of transformation")
    tone_x: Optional[int] = Field(0, ge=-100, le=100, description="Tone X-axis: formal(+) to casual(-), range: -100 to 100")
    tone_y: Optional[int] = Field(0, ge=-100, le=100, description="Tone Y-axis: concise(+) to elaborate(-), range: -100 to 100")
    format: Optional[FormatOption] = Field(None, description="Format transformation option")
    length: Optional[LengthOption] = Field(None, description="Length transformation option")
    target_language: Optional[LanguageOption] = Field(None, description="Target language")
    ai_provider: AIProvider = Field(AIProvider.GEMINI, description="AI model to use")
    custom_instruction: Optional[str] = Field(None, description="Additional instructions")


class FileUploadResponse(BaseModel):
    filename: str
    file_size: int
    extracted_text: str
    message: str


class TextTransformResponse(BaseModel):
    original_text: str
    transformed_text: str
    transformation_type: TransformationType
    ai_provider: AIProvider
    success: bool
    message: Optional[str] = None


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
