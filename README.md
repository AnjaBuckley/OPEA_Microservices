# OPEA Multi-Service AI Application

This project demonstrates how to run multiple AI services using OPEA (Open Protocol for Enterprise AI) components in Docker containers. It includes translation, text-to-speech, and embedding services orchestrated together with a Streamlit frontend.

## Architecture

The application consists of three microservices and a frontend:

1. **LLM Service** (Port 8000)
   - Handles English to German translation
   - Generates example sentences
   - Uses Helsinki-NLP/opus-mt-en-de model

2. **TTS Service** (Port 7002)
   - Converts German text to speech
   - Uses Google Text-to-Speech (gTTS)

3. **Embedding Service** (Port 6000)
   - Generates text embeddings
   - Demonstrates service separation

4. **Streamlit Frontend** (Port 8501)
   - User interface for interacting with services
   - Coordinates service communication

## Prerequisites

- Python 3.10 or higher
- Docker and Docker Compose
- Git

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd OPEA
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install watchdog  # For better Streamlit performance
   ```

4. **Build and Start Services**
   ```bash
   docker-compose build
   docker-compose up -d
   ```

5. **Run Streamlit App**
   ```bash
   streamlit run app.py
   ```

6. **Access the Application**
   - Open your browser and go to http://localhost:8501
   - The services will be available at:
     - LLM Service: http://localhost:8000
     - Embedding Service: http://localhost:6000
     - TTS Service: http://localhost:7002

## Project Structure

```
OPEA/
├── app.py                 # Streamlit frontend
├── docker-compose.yml     # Service orchestration
├── requirements.txt       # Python dependencies
├── services/
│   ├── embedding/        # Embedding service
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   ├── llm/             # Translation service
│   │   ├── Dockerfile
│   │   ├── app.py
│   │   └── requirements.txt
│   └── tts/             # Text-to-speech service
│       ├── Dockerfile
│       ├── app.py
│       └── requirements.txt
```

## Features

- English to German translation
- Natural German text-to-speech synthesis
- Example sentence generation
- Text embedding generation
- Containerized services
- Service orchestration with Docker Compose

## Development

To modify or extend the services:

1. Each service is independent and can be modified separately
2. Update the respective `requirements.txt` for new dependencies
3. Rebuild services with `docker-compose build`
4. Restart services with `docker-compose up -d`

## Troubleshooting

1. **Port Conflicts**
   - Ensure no other services are using ports 8501, 8000, 6000, or 7002
   - Kill existing Streamlit processes: `pkill -f streamlit`

2. **Service Health**
   - Check service logs: `docker-compose logs <service-name>`
   - Each service has a `/health` endpoint

3. **Common Issues**
   - If Streamlit port is in use, try a different port: `streamlit run app.py --server.port <port>`
   - If services are unresponsive, restart them: `docker-compose restart`

## Security Notes

1. Don't store sensitive data (API keys, credentials) in the repository
2. Use environment variables for configuration
3. Follow the `.gitignore` file to prevent sensitive data commits
4. Review Docker security best practices

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

[Your License Here]

## Acknowledgments

- OPEA Components Project
- Helsinki-NLP for the translation model
- Google Text-to-Speech
- Streamlit team

## Contact

[Your Contact Information] 