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

allowed_models = {'gpt-4o-mini', 'gpt-4', 'gpt-4o', 'gpt-3.5-turbo'}
model = 'gpt-4o-mini'

# Initialize Twilio client
twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

def handleModelChange(incoming_msg):
    global model
    new_model = incoming_msg.strip()[len('model: '):]
    if new_model in allowed_models:
        bot_reply = f'Successfully changed model to {new_model}'
        model = new_model
    else:
        bot_reply = f'{new_model} is not an allowed model'
    return bot_reply

def handleBilling(incoming_msg):
    # TODO: currently openai doesn't support this using the secret key. Only session keys (ie, from the browser) can make these requests.
    # https://api.openai.com/v1/dashboard/billing/subscription
    # https://api.openai.com/v1/dashboard/billing/usage?start_date={}&end_date={}
    return 'not implemented'

def handleChatGPTReply(incoming_msg):
    # Forward the message to ChatGPT
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": incoming_msg}
            ]
        )
        bot_reply = response.choices[0].message.content.strip()
    except Exception as e:
        bot_reply = f"I'm sorry, but I'm currently unable to process your request. Error: {e}"
    return bot_reply

@app.route('/webhook', methods=['POST'])
def webhook():
    sender_number = request.values.get('From', '').strip()
    incoming_msg = request.values.get('Body', '').strip()

    # Authenticate the sender
    if sender_number != AUTHORIZED_NUMBER:
        abort(403)  # Forbidden

    if incoming_msg.startswith('model: '):
        bot_reply = handleModelChange(incoming_msg)
    elif incoming_msg == 'billing':
        bot_reply = handleBilling(incoming_msg)
    else:
        bot_reply = handleChatGPTReply(incoming_msg)

    # Send the response back via WhatsApp
    twilio_resp = MessagingResponse()
    twilio_resp.message(body=bot_reply)
    return str(twilio_resp)

if __name__ == '__main__':
    # TODO: use a production WSGI server instead.
    # TODO: add other capabilities (eg. sending images, using other api providers, etc.) 
    app.run(host='0.0.0.0', port=5000)
