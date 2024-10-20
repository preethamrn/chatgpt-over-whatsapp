# ChatGPT Over Whatsapp (COW)

If you ever find yourself on an airplane where you're able to get free messaging but can't use Whatsapp, you've come to the right place.

ChatGPT Over Whatsapp (COW) will solve all your problems.

## Requirements

- python3
- docker
- A suitable hosting provider (eg. DigitalOcean)
- Twilio account
- OpenAI account

## Installation

Create a .env file with the following tokens.
```
# .env
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886  # Twilio sandbox number
OPENAI_API_KEY=your_openai_api_key
AUTHORIZED_NUMBER=whatsapp:+your_verified_number
```

### Set up Twilio
1. Create a Twilio account
2. On the Twilio console, make note of your Account SID and Auth Token in the .env file.
3. Navigate to **Messaging > Try it Out > Try Whatsapp**
4. Use WhatsApp and send a message from your device to +1 415 523 8886 with the given code. (Note: the TWILIO_WHATSAPP_NUMBER may be different)
5. If you get a response, you have successfully onboarded.

### Create an OpenAI API key
1. Navigate to https://platform.openai.com/api-keys
2. Create a new key and make note of it in the .env file
3. Add billing information. You can get a lot of tokens for just $5 using 4o-mini. I'd recommend turning off automatic recharge to avoid any unexpected bills.

## Testing

Start the web server container locally using docker by running
```
docker-compose up --build
```

Expose your testing machine to the web using a tool like ngrok
```
ngrok http 5000
```

Make note of the ngrok Forwarding URL. Let's say this is `https://5123.ngrok-free.app`. Set `https://5123.ngrok-free.app/webhook` in the Try Whatsapp Sandbox settings in Twilio.

Send a Whatsapp message to the Twilio Sandbox phone number, and see the response.

## Deployment

1. Clone this git repo on your hosting provider.
2. Copy the configuration in .env
3. Run `docker-compose up --build` and expose port 5000
4. Update the Sandbox settings URL in Twilio.

## Usage

TODO...