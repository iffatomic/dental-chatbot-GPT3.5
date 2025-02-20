from flask import Flask, render_template, request, jsonify
import time
import openai
import re

# Replace 'YOUR_API_KEY' with your actual OpenAI API key
api_key = ''

# Set the timestamp for the last request
last_request_time = time.time()
app = Flask(__name__)
chat_messages = []

# Define keywords related to dental healthcare
dental_keywords = ["oral", "teeth", "tooth", "flossing", "brush", "floss", "dentist", "toothache", "dental", "overbite",
                   "scaling", "toothbrush", "mouthwash", "cavities", "cavity", "gum disease", "bad breath", 
                   "braces", "toothpaste"]

@app.route('/')
def chatbot_interface():
    global chat_messages
    chat_messages = []

    initial_prompt = "Hello! Welcome to Dental Health Chatbot. I'm here to help you with your dental healthcare questions. Feel free to ask!"
    return render_template('chatbot.html', chat_messages=chat_messages, initial_prompt=initial_prompt)

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.json['user_input']
    print(f"User input: {user_input}")  # Debugging line

    # Check if the user input contains dental keywords using regex
    contains_keyword = any(re.search(rf"\b{keyword}\b", user_input.lower()) for keyword in dental_keywords)
    print(f"Contains dental keyword: {contains_keyword}")  # Debugging line

    if contains_keyword:
        chatbot_response = rate_limited_dental_chatbot(f"You: {user_input}\nDental Health Chatbot:")
        chatbot_response = chatbot_response.replace('\n', '<br>')  # Replace newlines with HTML line breaks
    else:
        chatbot_response = "I'm sorry, I can only answer questions about dental healthcare. Please ask me questions or rephrase your sentence regarding Dental Healthcare."

    # Update chat messages
    chat_messages.append(f"<div class='message user-message'><strong>You:</strong> {user_input}</div>")
    chat_messages.append(f"<div class='message chatbot-message'><strong>Dental Health Chatbot:</strong> {chatbot_response}</div>")

    return jsonify({'response': chatbot_response})

def rate_limited_dental_chatbot(prompt):
    global last_request_time

    # Get the current time and the time elapsed since the last request
    elapsed_time = time.time() - last_request_time

    if elapsed_time < 5:
        return "Please wait a few seconds before asking another question."

    last_request_time = time.time()

    openai.api_key = api_key
    response = openai.Completion.create(
        engine="gpt-3.5-turbo-instruct",
        prompt=prompt,
        max_tokens=250
    )
    
    return response.choices[0].text.strip()

if __name__ == '__main__':
    app.run(debug=True)
