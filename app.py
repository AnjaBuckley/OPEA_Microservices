import streamlit as st
import requests
from typing import Dict, List
import os
import base64
import io

# Service URLs
LLM_SERVICE_URL = os.getenv("LLM_SERVICE_URL", "http://localhost:8000")
EMBEDDING_SERVICE_URL = os.getenv("EMBEDDING_SERVICE_URL", "http://localhost:6000")
TTS_SERVICE_URL = os.getenv("TTS_SERVICE_URL", "http://localhost:7002")

st.set_page_config(page_title="OPEA Language Learning", page_icon="🗣️", layout="wide")

st.title("🗣️ OPEA Language Learning Assistant")
st.write("Learn German with AI-powered translation, examples, and pronunciation!")


# Check service health
def check_services():
    services = {
        "Translation": f"{LLM_SERVICE_URL}/health",
        "Embedding": f"{EMBEDDING_SERVICE_URL}/health",
        "Speech": f"{TTS_SERVICE_URL}/health",
    }

    all_healthy = True
    for name, url in services.items():
        try:
            response = requests.get(url)
            if response.status_code == 200:
                st.sidebar.success(f"✅ {name} Service: Healthy")
            else:
                st.sidebar.error(f"❌ {name} Service: Unhealthy")
                all_healthy = False
        except:
            st.sidebar.error(f"❌ {name} Service: Unavailable")
            all_healthy = False

    return all_healthy


# Sidebar
st.sidebar.title("Service Status")
services_healthy = check_services()

if not services_healthy:
    st.error(
        "⚠️ Some services are not available. Please check the service status in the sidebar."
    )
    st.stop()

# Main interface
tab1, tab2 = st.tabs(["Translation & Examples", "Practice"])

with tab1:
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("English Text")
        input_text = st.text_area("Enter English text to translate", height=150)

        if st.button("Translate"):
            if input_text:
                with st.spinner("Translating..."):
                    # Get translation
                    try:
                        response = requests.post(
                            f"{LLM_SERVICE_URL}/translate",
                            json={
                                "text": input_text,
                                "source_language": "en",
                                "target_language": "de",
                            },
                        )
                        translation_result = response.json()

                        # Store translation for examples
                        st.session_state.last_translation = translation_result[
                            "translated_text"
                        ]
                        st.session_state.last_input = input_text

                        # Get embedding for visualization
                        embed_response = requests.post(
                            f"{EMBEDDING_SERVICE_URL}/embed", json={"text": input_text}
                        )
                        embedding = embed_response.json()["embedding"]

                        # Generate speech
                        tts_response = requests.post(
                            f"{TTS_SERVICE_URL}/synthesize",
                            json={
                                "text": translation_result["translated_text"],
                                "language": "de",
                            },
                        )
                        tts_result = tts_response.json()

                        # Store audio data
                        st.session_state.last_audio = tts_result["audio_data"]
                        st.session_state.last_audio_format = tts_result["format"]

                    except Exception as e:
                        st.error(f"Error: {str(e)}")
                        st.stop()
            else:
                st.warning("Please enter some text to translate.")

    with col2:
        st.subheader("German Translation")
        if "last_translation" in st.session_state:
            st.text_area("Translation", st.session_state.last_translation, height=150)
            if "last_audio" in st.session_state:
                # Convert base64 audio data to bytes
                audio_bytes = base64.b64decode(st.session_state.last_audio)
                st.audio(audio_bytes, format=st.session_state.last_audio_format)

            # Get example sentences
            if st.button("Show Examples"):
                with st.spinner("Generating examples..."):
                    try:
                        response = requests.post(
                            f"{LLM_SERVICE_URL}/examples",
                            json={
                                "text": st.session_state.last_input,
                                "language": "de",
                            },
                        )
                        examples = response.json()["examples"]
                        st.subheader("Example Sentences")
                        st.write(examples)

                    except Exception as e:
                        st.error(f"Error generating examples: {str(e)}")

with tab2:
    st.subheader("Practice Section")
    st.info(
        "Coming soon! This section will include interactive exercises and pronunciation practice."
    )
