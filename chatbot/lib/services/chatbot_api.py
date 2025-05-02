from flask import Flask, request, jsonify
import re
import random

app = Flask(__name__)

class RuleBot:
    negative_responses = ("no", "nope", "nah", "naw", "not a chance", "sorry")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")
    random_questions = (
        "Why are you here?",
        "Are there many humans like you?",
        "What do you consume for sustenance?",
        "Is there intelligent life on this planet?",
        "Does Earth have a leader?",
        "What planets have you visited?",
        "What technology do you have on this planet?"
    )

    def __init__(self):
        self.alienbabble = {
            'describe_planet_intent': r'.*\s*your\s*planet.*',
            'answer_why_intent': r'why\sare.*',
            'about_intellipat': r'.*\s*intellipat.*'
        }
        self.name = ""
        self.state = 'ask_name'

    def get_response(self, user_message):
        user_message = user_message.lower().strip()

        if self.is_exit_command(user_message):
            self.state = 'exit'
            return "Goodbye! Have a great day."

        if self.state == 'ask_name':
            self.state = 'greet'
            return "Hello! What's your name?"

        elif self.state == 'greet':
            self.name = user_message.capitalize()
            self.state = 'chatting'
            return f"Nice to meet you {self.name}, nasılsın bugün?"

        elif self.state == 'chatting':
            if self.is_negative(user_message):
                return "I'm sorry to hear that, {self.name}. Is there anything I can do to help?"
            elif self.is_positive(user_message):
                return "That's great to hear {self.name}! Is there something you'd like to talk about?"

            return self.match_reply(user_message)

        elif self.state == 'exit':
            return "The conversation has ended. I'm here if you want to talk again!"

        return "Something went wrong."

    def is_exit_command(self, message):
        return any(message == cmd for cmd in self.exit_commands)

    def is_negative(self, message):
        return any(word in message for word in self.negative_responses)


    def is_positive(self, message):
        return message in ("yes", "yeah", "yep", "sure", "of course", "ok")

    def match_reply(self, reply):
        for key, value in self.alienbabble.items():
            if re.match(value, reply):
                if key == 'describe_planet_intent':
                    return self.describe_planet_intent()
                elif key == 'answer_why_intent':
                    return self.answer_why_intent()
                elif key == 'about_intellipat':
                    return self.about_intellipat()
        return self.no_match_intent()

    def describe_planet_intent(self):
        responses = (
            "My planet is a utopia of diverse organisms and species.",
            "I am from Opidipus, the capital of the Wayward Galaxies."
        )
        return random.choice(responses)

    def answer_why_intent(self):
        responses = (
            "I come in peace.",
            "I am here to collect data on your planet and its inhabitants.",
            "I heard the coffee is good."
        )
        return random.choice(responses)

    def about_intellipat(self):
        responses = (
            "Intellipaat is the world's largest professional educational company.",
            "Intellipaat helps you learn concepts in a whole new way.",
            "Intellipaat is where your career and skills grow."
        )
        return random.choice(responses)

    def no_match_intent(self):
        responses = (
            "Could you elaborate on that?",
        "That's interesting. Can you tell me more?",
        "Hmm, what else is on your mind?",
        "Please go on, I'd love to hear more."
        )
        return random.choice(responses)
    
bot = RuleBot()

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "No message received!"}), 400

    # Bot objesini oluşturuyoruz ve mesajı yanıtlıyoruz
    
    response = bot.get_response(user_message)

    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # 0.0.0.0, dışarıdan erişime izin verir bu şekilde
