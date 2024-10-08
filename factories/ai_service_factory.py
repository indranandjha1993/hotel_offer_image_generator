from contaracts.ai_contract import TextGenerationService, ImageGenerationService
from services.openai_service import OpenAITextService, OpenAIImageService


# from services.aws_bedrock_service import AWSBedrockTextService, AWSBedrockImageService
# from services.ollama_service import OllamaTextService, OllamaImageService


class AIServiceFactory:
    @staticmethod
    def get_text_service(service_name: str) -> TextGenerationService:
        if service_name == "openai":
            return OpenAITextService()
        # elif service_name == "aws_bedrock":
        #     return AWSBedrockTextService()
        # elif service_name == "ollama":
        #     return OllamaTextService()
        else:
            raise ValueError(f"Unknown text service: {service_name}")

    @staticmethod
    def get_image_service(service_name: str) -> ImageGenerationService:
        if service_name == "openai":
            return OpenAIImageService()
        # elif service_name == "aws_bedrock":
        #     return AWSBedrockImageService()
        # elif service_name == "ollama":
        #     return OllamaImageService()
        else:
            raise ValueError(f"Unknown image service: {service_name}")
