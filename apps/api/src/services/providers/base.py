from abc import ABC, abstractmethod
from typing import Optional
from ...models.schemas import TransformationType, FormatOption, LengthOption, LanguageOption


class BaseAIProvider(ABC):
    """Base interface for AI providers"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
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
        """Transform text using the AI provider."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the AI provider is available."""
        pass
    
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
        """Build prompt for the AI model."""
        
        prompt_parts = []
        
        # Basic instructions
        if transformation_type == TransformationType.TONE:
            tone_instructions = []
            
            # Handle X-axis (formal/casual)
            if tone_x > 0:
                intensity = "slightly" if tone_x <= 30 else "moderately" if tone_x <= 60 else "very"
                tone_instructions.append(f"Make the text {intensity} formal and professional")
            elif tone_x < 0:
                intensity = "slightly" if abs(tone_x) <= 30 else "moderately" if abs(tone_x) <= 60 else "very"
                tone_instructions.append(f"Make the text {intensity} casual and conversational")
            
            # Handle Y-axis (concise/elaborate)
            if tone_y > 0:
                intensity = "slightly" if tone_y <= 30 else "moderately" if tone_y <= 60 else "very"
                tone_instructions.append(f"Make the text {intensity} concise and brief")
            elif tone_y < 0:
                intensity = "slightly" if abs(tone_y) <= 30 else "moderately" if abs(tone_y) <= 60 else "very"
                tone_instructions.append(f"Make the text {intensity} elaborate and detailed")
            
            if tone_instructions:
                prompt_parts.append("Please transform the following text with these tone adjustments:")
                prompt_parts.append("- " + "\n- ".join(tone_instructions))
            else:
                # (0, 0) - neutral, no tone transformation
                prompt_parts.append("Please keep the original tone of the text.")
        
        elif transformation_type == TransformationType.FORMAT and format:
            format_instructions = {
                FormatOption.EMAIL: "Please transform the following text to email format.",
                FormatOption.REPORT: "Please transform the following text to report format.",
                FormatOption.SNS: "Please transform the following text to social media post format.",
                FormatOption.BLOG: "Please transform the following text to blog post format.",
                FormatOption.SUMMARY: "Please transform the following text to summary format."
            }
            prompt_parts.append(format_instructions.get(format, "Please change the format."))
        
        elif transformation_type == TransformationType.LENGTH and length:
            length_instructions = {
                LengthOption.EXPAND: "Please expand the following text with more details and make it longer.",
                LengthOption.SUMMARIZE: "Please summarize the following text concisely.",
                LengthOption.MAINTAIN: "Please improve the content while maintaining the length of the following text."
            }
            prompt_parts.append(length_instructions.get(length, "Please adjust the length."))
        
        elif transformation_type == TransformationType.LANGUAGE and target_language:
            language_names = {
                LanguageOption.KOREAN: "Korean",
                LanguageOption.ENGLISH: "English",
                LanguageOption.JAPANESE: "Japanese",
                LanguageOption.CHINESE: "Chinese"
            }
            target_lang_name = language_names.get(target_language, "target language")
            prompt_parts.append(f"Please translate the following text to {target_lang_name}.")
        
        # Add custom instructions
        if custom_instruction:
            prompt_parts.append(f"Additional requirements: {custom_instruction}")
        
        # Add text to transform
        prompt_parts.append(f"\nText to transform:\n{text}")
        
        return "\n\n".join(prompt_parts)
