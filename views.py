# mysite/fb_championsbot/views.py
import json, requests, random, re
from pprint import pprint

from django.views import generic
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

PAGE_ACCESS_TOKEN = "EAAX8vNyWoNcBAPTZBar1u0v85A9Mc9kH4dCWZB9veZA4f1qs81UbaicItLVkODnKGT9HHNMZCa0lsqv4dC23yelYIo0t4EWwdjDq2DTqmnUBlacarJIKZCH8G17LC9ZAh3kl2iyXEVtyE5s2bJRydHvJjvVkZBT5eQPMASW7dJZAAAZDZD"
VERIFY_TOKEN = "19041971"

soccerAnswer = { '2003': ["""Milan won in Manchester beating Juventus :) """,
                     """Come on!! it was Milan with the final penalty from Shevchenko """], 
         '2005': ["""Milan took revenge of Liverpool and beat them 2-1.""",
                  """In Athens, Milan beat Liverpool"""],
          '2007': ["""Milan took revenge of Liverpool and beat them 2-1.""",
                   """In Athens, Milan beat Liverpool"""],
          '2014': ["""Real Madrid won la decima agains Atletico Madrid for 4-1""",
                   """Atletico was 1-0 at the 89' then Sergio Ramos tied. """],
          '2015': ["Barca beat juve",
                  "Juve lost again with Barcelona"],
          '2016': ["""Real Madrid didn't allow Atletico Madrid to take revenge and it won at the penalty kicks.""",
                   "In Milan, Real Madrid defeated Atletico again."],
          }

# Helper function
def post_facebook_message(fbid, recevied_message):
    # Remove all punctuations, lower case the text and split it based on space
    tokens = re.sub(r"[^a-zA-Z0-9\s]",' ',recevied_message).lower().split()
    soccerAnswer_text = ''
    for token in tokens:
        if token in soccerAnswer:
            soccerAnswer_text = random.choice(soccerAnswer[token])
            break
    if not soccerAnswer_text:
        soccerAnswer_text = "Type me any year and I will tell you who won the Champions League!"

    user_details_url = "https://graph.facebook.com/v2.6/%s"%fbid 
    user_details_params = {'fields':'first_name,last_name,profile_pic', 'access_token':PAGE_ACCESS_TOKEN} 
    user_details = requests.get(user_details_url, user_details_params).json()
    soccerAnswer_text = 'Hey '+user_details['first_name']+'! ' + soccerAnswer_text
                   
    post_message_url = 'https://graph.facebook.com/v2.6/me/messages?access_token=%s'%PAGE_ACCESS_TOKEN
    response_msg = json.dumps({"recipient":{"id":fbid}, "message":{"text":soccerAnswer_text}})
    status = requests.post(post_message_url, headers={"Content-Type": "application/json"},data=response_msg)
    pprint(status.json())


class ChampionsBotView(generic.View):
    def get(self, request, *args, **kwargs):
        if self.request.GET['hub.verify_token'] == VERIFY_TOKEN:
            return HttpResponse(self.request.GET['hub.challenge'])
        else:
            return HttpResponse('Error, invalid token')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    # Post function to handle messages in Facebook
    def post(self, request, *args, **kwargs):
        incoming_message = json.loads(self.request.body.decode('utf-8'))
        for entry in incoming_message['entry']:
            for message in entry['messaging']:
                if 'message' in message:
                    pprint(message)
                    post_facebook_message(message['sender']['id'], message['message']['text'])     
        return HttpResponse()

