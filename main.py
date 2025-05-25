import requests
import base64
import os
from dotenv import load_dotenv
from prompt_template import wellNessPromptTemplate

# Load environment variables from .env file if it exists
load_dotenv()

class WellnessBot:
    def __init__(self):
        self.invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
        self.stream = True
        self.headers = {
            "Authorization": f"Bearer {os.getenv('NVIDIA_API_KEY', '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')}",
            "Accept": "text/event-stream" if self.stream else "application/json"
        }
        self.conversation_history = []
        
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
    def add_message(self, role, content):
        self.conversation_history.append({"role": role, "content": content})
        
    def prepare_messages(self, user_input):
        # First message always includes our system prompt with the wellness template
        messages = [{"role": "system", "content": wellNessPromptTemplate("")}]
        
        # Add conversation history (up to last 6 messages to keep context reasonable)
        history = self.conversation_history[-6:] if len(self.conversation_history) > 6 else self.conversation_history
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
            "stream": self.stream
        }
        
        response = requests.post(self.invoke_url, headers=self.headers, json=payload)
        
        if self.stream:
            full_response = ""
            print("\nWellnessBot: ", end="", flush=True)
            for line in response.iter_lines():
                if line:
                    line_text = line.decode("utf-8")
                    if line_text.startswith("data:") and line_text != "data: [DONE]":
                        try:
                            # Extract actual content from the streaming response
                            content_part = line_text.replace("data:", "").strip()
                            if "[DONE]" not in content_part and content_part:
                                import json
                                json_data = json.loads(content_part)
                                if "choices" in json_data and json_data["choices"]:
                                    if "delta" in json_data["choices"][0] and "content" in json_data["choices"][0]["delta"]:
                                        chunk = json_data["choices"][0]["delta"]["content"]
                                        print(chunk, end="", flush=True)
                                        full_response += chunk
                        except Exception as e:
                            pass
            print("\n")
            # Add bot response to conversation history
            self.add_message("assistant", full_response)
            return full_response
        else:
            response_json = response.json()
            bot_response = response_json["choices"][0]["message"]["content"]
            self.add_message("assistant", bot_response)
            print(f"\nWellnessBot: {bot_response}\n")
            return bot_response

    def run(self):
        self.clear_screen()
        print("="*50)
        print("🌿 Welcome to WellnessBot 🌿")
        print("Your AI companion for health and wellness advice.")
        print("Type 'exit' to quit the conversation.")
        print("="*50)
        
        while True:
            user_input = input("\nYou: ")
            if user_input.lower() in ['exit', 'quit', 'bye']:
                print("\nWellnessBot: Thank you for chatting! Take care and stay well! 🌱")
                break
                
            # Add user message to history
            self.add_message("user", user_input)
            
            # Get and display bot response
            self.get_wellness_advice(user_input)


if __name__ == "__main__":
    bot = WellnessBot()
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\nThank you for using WellnessBot! Goodbye!")
