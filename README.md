# 🌿 WellnessBot

WellnessBot is an AI-powered chatbot that provides personalized wellness advice, including information on physical health, mental well-being, nutrition, fitness, and lifestyle choices.

## Features

- Interactive command-line and web interfaces
- Personalized wellness recommendations
- Evidence-based health information
- Conversation memory to maintain context
- Streaming responses for a more natural conversation flow (CLI version)
- Modern, user-friendly web interface (Streamlit version)

## Requirements

- Python 3.6+
- Required packages (see `requirements.txt`):
  - requests
  - streamlit
  - python-dotenv

## Usage

### Command Line Interface

To start the WellnessBot in command-line mode:

```bash
python main.py
```

Interact with the bot by typing your wellness-related questions when prompted. The bot will respond with helpful information and advice.

Type `exit`, `quit`, or `bye` to end the conversation.

### Web Interface (Streamlit)

To run the WellnessBot with the Streamlit web interface:

```bash
streamlit run app.py
```

This will start a local web server and open your browser to the WellnessBot web interface. You can then interact with the bot through the chat interface in your web browser.

## Technical Details

WellnessBot uses NVIDIA's API to connect with the Mistral Medium 3 language model, providing high-quality, contextually relevant responses to wellness queries.

## Customization

You can modify the prompt template in `prompt_template.py` to adjust the bot's personality and response style.

## License

This project is for personal use only. API keys should not be shared.

## Disclaimer

WellnessBot provides general wellness information and should not be considered a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.