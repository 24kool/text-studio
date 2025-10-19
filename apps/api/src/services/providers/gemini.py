import google.generativeai as genai
from typing import Optional
from .base import BaseAIProvider
from ...models.schemas import TransformationType, ToneOption, FormatOption, LengthOption, LanguageOption


class GeminiProvider(BaseAIProvider):
    """Google Gemini API provider"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    async def transform_text(
        self,
        text: str,
        transformation_type: TransformationType,
        tone_x: Optional[int] = 0,
        tone_y: Optional[int] = 0,
        format: Optional[FormatOption] = None,
        length: Optional[LengthOption] = None,
        target_language: Optional[LanguageOption] = None,
        custom_instruction: Optional[str] = None
    ) -> str:
        """Transform text using Gemini API."""
        
        prompt = self._build_prompt(
            text, transformation_type, tone_x, tone_y, format, length, target_language, custom_instruction
        )
        
        try:
            response = await self.model.generate_content_async(prompt)
            return response.text.strip()
        except Exception as e:
            raise Exception(f"Error calling Gemini API: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Gemini API is available."""
        return bool(self.api_key)
    
    def _build_prompt(
        self,
        text: str,
        transformation_type: TransformationType,
        tone_x: Optional[int] = 0,
        tone_y: Optional[int] = 0,
        format: Optional[FormatOption] = None,
        length: Optional[LengthOption] = None,
        target_language: Optional[LanguageOption] = None,
        custom_instruction: Optional[str] = None
    ) -> str:
        """Build Gemini-specific prompt."""
        
        base_prompt = super()._build_prompt(
            text, transformation_type, tone_x, tone_y, format, length, target_language, custom_instruction
        )
        
        # Add Gemini-specific instructions
        gemini_instruction = """
Please return only the transformed text. Do not include additional explanations or comments.
Perform the requested transformation while maintaining the core meaning of the original text.
"""
        
        return gemini_instruction + "\n" + base_prompt
