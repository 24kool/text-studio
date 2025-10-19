from typing import Optional, Dict
from ..models.schemas import (
    AIProvider, TransformationType, ToneOption, FormatOption, 
    LengthOption, LanguageOption
)
from .providers.base import BaseAIProvider
from .providers.gemini import GeminiProvider
from ..config.settings import settings


class AIService:
    """AI service abstraction layer"""
    
    def __init__(self):
        self._providers: Dict[AIProvider, BaseAIProvider] = {}
        self._initialize_providers()
    
    def _initialize_providers(self):
        """Initialize available AI providers."""
        
        # Initialize Gemini provider
        if settings.gemini_api_key:
            self._providers[AIProvider.GEMINI] = GeminiProvider(settings.gemini_api_key)
        
        # Future providers can be added here
        # if settings.openai_api_key:
        #     self._providers[AIProvider.OPENAI] = OpenAIProvider(settings.openai_api_key)
    
    def get_available_providers(self) -> list[AIProvider]:
        """Return list of available AI providers."""
        return [
            provider for provider, instance in self._providers.items() 
            if instance.is_available()
        ]
    
    def get_provider(self, provider: AIProvider) -> BaseAIProvider:
        """Return specific AI provider."""
        if provider not in self._providers:
            raise ValueError(f"Provider '{provider}' not found.")
        
        if not self._providers[provider].is_available():
            raise ValueError(f"Provider '{provider}' is not available.")
        
        return self._providers[provider]
    
    async def transform_text(
        self,
        text: str,
        transformation_type: TransformationType,
        provider: AIProvider = None,
        tone: Optional[ToneOption] = None,
        format: Optional[FormatOption] = None,
        length: Optional[LengthOption] = None,
        target_language: Optional[LanguageOption] = None,
        custom_instruction: Optional[str] = None
    ) -> str:
        """Transform text using AI provider."""
        
        # Set default provider
        if provider is None:
            available_providers = self.get_available_providers()
            if not available_providers:
                raise ValueError("No available AI providers.")
            provider = available_providers[0]  # Use first available provider
        
        ai_provider = self.get_provider(provider)
        
        return await ai_provider.transform_text(
            text=text,
            transformation_type=transformation_type,
            tone=tone,
            format=format,
            length=length,
            target_language=target_language,
            custom_instruction=custom_instruction
        )


# Singleton instance
ai_service = AIService()
