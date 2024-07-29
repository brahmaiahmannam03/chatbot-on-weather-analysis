from flask import Flask, request, jsonify
import nltk
from nltk.chat.util import Chat, reflections
import requests

# Download NLTK data files (only need to do this once)
nltk.download('punkt')

# Define conversation patterns
pairs = [
    ['my name is (.*)', ['Hello %1, how can I help you today?']],
    ['(hi|hello|hey)', ['Hello!', 'Hey there!']],
    ['what is your name?', ['I am a chatbot created by [Your Name].']],
    ['how are you?', ['I am good, thank you! How are you?']],
    ['quit', ['Goodbye! Have a nice day.']],
    ['weather in (.*)', ['Fetching weather information for %1...']]
]

chat = Chat(pairs, reflections)

# Initialize Flask app
app = Flask(__name__)

def get_weather(city):
    api_key = '8edc19eb711000ab20541b1affa48f26'  # Replace with your actual API key
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        
        return (f"The weather in {city} is currently {weather_description} with a temperature of "
                f"{temperature}°C, feels like {feels_like}°C, and humidity of {humidity}%.")
    else:
        return "Sorry, I couldn't fetch the weather information at the moment."

@app.route('/')
def home():
    return "Chatbot is running. Send messages to /chat."

@app.route('/chat', methods=['POST'])
def chat_response():
    user_message = request.json.get('message')
    
    # Check if the user is asking about the weather
    if user_message.lower().startswith('weather in '):
        city = user_message[11:].strip()  # Extract the city name from the user message and strip any extra spaces
        response = get_weather(city)
    else:
        # Use the chatbot's response for other messages
        response = chat.respond(user_message)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)
