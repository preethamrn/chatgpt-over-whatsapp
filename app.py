from flask import Flask, request, abort
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import openai
import os

app = Flask(__name__)

# Load environment variables
openai.api_key = os.environ.get('OPENAI_API_KEY')
AUTHORIZED_NUMBER = os.environ.get('AUTHORIZED_NUMBER')
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.environ.get('TWILIO_WHATSAPP_NUMBER')

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@app.route('/webhook', methods=['POST'])
def webhook():
    sender_number = request.values.get('From', '').strip()
    incoming_msg = request.values.get('Body', '').strip()

    # Authenticate the sender
    if sender_number != AUTHORIZED_NUMBER:
        abort(403)  # Forbidden

    # Forward the message to ChatGPT
    try:
        response = openai.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {"role": "user", "content": incoming_msg}
            ]
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        bot_reply = f"I'm sorry, but I'm currently unable to process your request. Error: {e}"

    # Send the response back via WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(body=bot_reply)
    return str(twilio_resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
