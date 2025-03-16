import os
from comps import MicroService, ServiceOrchestrator, ServiceType, TextDoc

# Service connection details from environment variables
LLM_SERVICE_HOST = os.getenv("LLM_SERVICE_HOST", "llm-service")
LLM_SERVICE_PORT = int(os.getenv("LLM_SERVICE_PORT", 9000))
EMBEDDING_SERVICE_HOST = os.getenv("EMBEDDING_SERVICE_HOST", "embedding-service")
EMBEDDING_SERVICE_PORT = int(os.getenv("EMBEDDING_SERVICE_PORT", 6000))
TTS_SERVICE_HOST = os.getenv("TTS_SERVICE_HOST", "tts-service")
TTS_SERVICE_PORT = int(os.getenv("TTS_SERVICE_PORT", 7000))


class GermanLearningService:
    def __init__(self, host="0.0.0.0", port=8000):
        self.host = host
        self.port = port
        self.megaservice = ServiceOrchestrator()
        self.setup_services()

    def setup_services(self):
        # Create microservice connections
        llm = MicroService(
            name="language_model",
            host=LLM_SERVICE_HOST,
            port=LLM_SERVICE_PORT,
            endpoint="/v1/chat/completions",
            use_remote_service=True,
            service_type=ServiceType.LLM,
        )

        embedding = MicroService(
            name="semantic_search",
            host=EMBEDDING_SERVICE_HOST,
            port=EMBEDDING_SERVICE_PORT,
            endpoint="/v1/embeddings",
            use_remote_service=True,
            service_type=ServiceType.EMBEDDING,
        )

        tts = MicroService(
            name="speech_synthesis",
            host=TTS_SERVICE_HOST,
            port=TTS_SERVICE_PORT,
            endpoint="/v1/tts",
            use_remote_service=True,
            service_type=ServiceType.TTS,
        )

        # Add services to orchestrator
        self.megaservice.add(llm).add(embedding).add(tts)

        # Define service flows
        self.megaservice.flow_to(embedding, llm)
        self.megaservice.flow_to(llm, tts)

    def translate(self, text):
        """Translate English to German"""
        response = self.megaservice.services["language_model"].request(
            method="POST",
            json={
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a German language translation assistant.",
                    },
                    {
                        "role": "user",
                        "content": f"Translate the following to German: {text}",
                    },
                ],
                "temperature": 0.3,
            },
        )
        return response.json()["choices"][0]["message"]["content"]

    def get_examples(self, concept):
        """Get example sentences for a German concept"""
        response = self.megaservice.services["language_model"].request(
            method="POST",
            json={
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a German language teaching assistant.",
                    },
                    {
                        "role": "user",
                        "content": f"Give me 3 example sentences using the German concept: {concept}",
                    },
                ],
                "temperature": 0.7,
            },
        )
        return response.json()["choices"][0]["message"]["content"]

    def pronounce(self, text):
        """Generate audio for German text"""
        response = self.megaservice.services["speech_synthesis"].request(
            method="POST", json={"text": text, "language": "de"}
        )
        return response.content  # Binary audio data
