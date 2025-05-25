# 🌿 WellnessBot

WellnessBot is an AI-powered chatbot that provides personalized wellness advice, including information on physical health, mental well-being, nutrition, fitness, and lifestyle choices.

## Demo

[<video controls src="Demo.mp4" title="Title"></video>](https://github.com/user-attachments/assets/fd4108ca-9143-4ab3-8c23-7e5573c212c1)

## Features

- Modern, user-friendly web interface (Streamlit)
- Personalized wellness recommendations
- Evidence-based health information
- Conversation memory to maintain context
- Interactive chat experience

## Requirements

- Python 3.13+
- Required packages (see `requirements.txt`):
  - requests
  - streamlit
  - python-dotenv

## Usage

To run the WellnessBot:

```bash
streamlit run app.py
```

This will start a local web server and open your browser to the WellnessBot web interface. You can then interact with the bot through the chat interface in your web browser.

### Fork and Customize

To use or customize WellnessBot, fork this repository and clone it to your local machine:

```bash
git clone https://github.com/Pratham-gupta-235/WellnessBot.git
cd WellnessBot
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

You can then run the bot or modify the code to suit your needs.

## Technical Details

WellnessBot uses NVIDIA's API to connect with the Mistral Medium 3 language model, providing high-quality, contextually relevant responses to wellness queries.

## Customization

You can modify the prompt template in `prompt_template.py` to adjust the bot's personality and response style.

## Disclaimer

WellnessBot provides general wellness information and should not be considered a substitute for professional medical advice, diagnosis, or treatment. Always consult with qualified healthcare providers for medical concerns.
