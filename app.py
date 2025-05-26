import os
import requests
import streamlit as st
from dotenv import load_dotenv
from src.prompt_template import wellNessPromptTemplate

# Load environment variables
load_dotenv()


class StreamlitWellnessBot:
    def __init__(self):
        self.invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"

        self.api_key = os.getenv("API_KEY")
        if not self.api_key:
            raise ValueError("API_KEY environment variable not set.")

        self.model_name = os.getenv("MODEL_NAME")
        if not self.model_name:
            raise ValueError("MODEL_NAME environment variable not set.")

        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        self.max_tokens = int(os.getenv("MAX_TOKENS", 1024))
        self.temperature = float(os.getenv("TEMPERATURE", 0.7))

    def prepare_messages(self, user_input):
        history = st.session_state.get("conversation_history", [])
        messages = [{"role": "system", "content": wellNessPromptTemplate("")}]
        messages.extend(history[-6:])
        messages.append({"role": "user", "content": user_input})
        return messages

    def get_wellness_advice(self, user_input):
        messages = self.prepare_messages(user_input)
        payload = {
            "model": self.model_name,
            "messages": messages,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": False
        }

        try:
            response = requests.post(self.invoke_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            bot_reply = (
                data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "No response content received.")
            )

            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            st.session_state.conversation_history.append({"role": "assistant", "content": bot_reply})

            return bot_reply

        except Exception as e:
            return f"Error: {str(e)}"


def initialize_session_state():
    st.session_state.setdefault("conversation_history", [])
    st.session_state.setdefault("messages", [])


def display_chat_history():
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])


def handle_user_input():
    if user_input := st.chat_input("Ask about health and wellness..."):
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot = StreamlitWellnessBot()
                response = bot.get_wellness_advice(user_input)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


def main():
    st.set_page_config(page_title="WellnessBot 🌿", page_icon="🌿", layout="centered")
    initialize_session_state()

    st.title("🌿 WellnessBot 🌿")
    st.subheader("Your AI companion for health and wellness advice")

    with st.sidebar:
        st.title("About WellnessBot")
        st.markdown("""
            WellnessBot is an AI-powered assistant that provides evidence-based information on:<br>
            🖋️ Physical health and fitness <br>
            🧠 Mental well-being <br>
            🥗 Nutrition and diet <br>
            🏃 Lifestyle choices <br>
            🧘 Self-care practices <br><br>
            <small><i>The bot uses a large language model to provide personalized wellness advice.<br>
            This is not a substitute for professional medical guidance.</i></small>
        """, unsafe_allow_html=True)

    display_chat_history()
    handle_user_input()
    st.divider()


if __name__ == "__main__":
    main()
