import requests
import json

from twilio.rest import Client
from flask import Flask, request, redirect

app = Flask(__name__)

#enter twilio details here
account_sid = '[Twilio_SID]'
auth_token = '[Twilio_TOKEN]'
client = Client(account_sid, auth_token)


@app.route("/whatsapp", methods=['POST'])
def whatsapp():
    message_body = request.form['Body'].lower()
    sender = request.form['From']
    response = ""

    if 'hi' in message_body or 'hello' in message_body or 'hola' in message_body:
        response = "Hi! Are you a vegetarian or non-vegetarian? Please reply with 'veg' or 'non-veg'."
    elif 'veg' in message_body:
        #enter spoonacular api key in 'API_KEY'
        url = 'https://api.spoonacular.com/recipes/random?apiKey=[API_KEY]&number=1&tags=vegetarian'
        response = get_recipe(url)
    elif 'non-veg' in message_body:
        url = 'https://api.spoonacular.com/recipes/random?apiKey=[API_KEY]&number=1&tags='
        response = get_recipe(url)
    else:
        response = "I'm sorry, I didn't understand your message. Please reply with 'veg' or 'non-veg'."

    send_message(sender, response)

    return redirect("/", code=302)


def get_recipe(url):
    response = requests.get(url)
    recipe = json.loads(response.text)['recipes'][0]
    recipe_title = recipe['title']
    recipe_link = recipe['spoonacularSourceUrl']
    recipe_text = f"{recipe_title}\n\n{recipe_link}"
    return recipe_text


def send_message(sender, message):
    message = client.messages.create(
        to=sender,
        #Enter Twilio number
        from_='[Twilio_NUMBER]',
        body=message
    )


if __name__ == "__main__":
    app.run()
