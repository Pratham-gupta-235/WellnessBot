import streamlit as st
import requests
import json
import os
from dotenv import load_dotenv
from src.prompt_template import wellNessPromptTemplate

# Load environment variables from .env file if it exists
load_dotenv()

class StreamlitWellnessBot:
    def __init__(self):
        self.invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY', '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')}",
            "Content-Type": "application/json"
        }
        
    def prepare_messages(self, user_input):
        # Get conversation history from session state
        conversation_history = st.session_state.get("conversation_history", [])
        
        # First message always includes our system prompt with the wellness template
        messages = [{"role": "system", "content": wellNessPromptTemplate("")}]
        
        # Add conversation history (up to last 6 messages to keep context reasonable)
        history = conversation_history[-6:] if len(conversation_history) > 6 else conversation_history
        messages.extend(history)
        
        # Add the current user message
        messages.append({"role": "user", "content": user_input})
        
        return messages

    def get_wellness_advice(self, user_input):
        messages = self.prepare_messages(user_input)
        payload = {
            "model": os.getenv('MODEL_NAME', 'mistralai/mistral-medium-3-instruct'),
            "messages": messages,
            "max_tokens": int(os.getenv('MAX_TOKENS', 1024)),
            "temperature": float(os.getenv('TEMPERATURE', 0.7)),
            "top_p": 0.9,
            "frequency_penalty": 0.0,
            "presence_penalty": 0.0,
            "stream": False
        }
        
        try:
            response = requests.post(self.invoke_url, headers=self.headers, json=payload)
            response.raise_for_status()
            response_json = response.json()
            bot_response = response_json["choices"][0]["message"]["content"]
            
            # Update conversation history in session state
            if "conversation_history" not in st.session_state:
                st.session_state.conversation_history = []
            
            st.session_state.conversation_history.append({"role": "user", "content": user_input})
            st.session_state.conversation_history.append({"role": "assistant", "content": bot_response})
            
            return bot_response
            
        except Exception as e:
            return f"Sorry, there was an error processing your request: {str(e)}"

def initialize_session_state():
    if "conversation_history" not in st.session_state:
        st.session_state.conversation_history = []
    if "messages" not in st.session_state:
        st.session_state.messages = []

def display_chat_history():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    if prompt := st.chat_input("Ask about health and wellness..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
            
        # Get bot response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                bot = StreamlitWellnessBot()
                response = bot.get_wellness_advice(prompt)
                st.markdown(response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

def main():
    st.set_page_config(page_title="🌿 WellnessBot", page_icon="🌿", layout="centered")
    
    # Initialize session state
    initialize_session_state()
    
    # Header
    st.title("🌿 WellnessBot 🌿")
    st.subheader("Your AI companion for health and wellness advice")
    
    # Add description in sidebar
    with st.sidebar:
        st.header("About WellnessBot")
        st.write("""
        WellnessBot is an AI-powered assistant that provides evidence-based information on:
        - Physical health and fitness
        - Mental well-being
        - Nutrition and diet
        - Lifestyle choices
        - Self-care practices
        
        The bot uses a large language model to provide personalized wellness advice.
        Please note that while the information is helpful, it should not replace professional medical advice.
        """)
    
    # Display chat interface
    st.divider()
    display_chat_history()
    handle_user_input()
    
    # Footer
    st.divider()
    st.caption("WellnessBot is powered by NVIDIA API and Mistral AI. It provides general wellness information and should not be considered medical advice.")

if __name__ == "__main__":
    main()
