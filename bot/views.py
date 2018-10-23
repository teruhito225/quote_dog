from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from .models import Quote
import random
import os

LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(LINE_CHANNEL_SECRET)

from django.shortcuts import render

def index(request):
    return HttpResponse("This is bot api.")

@csrf_exempt
def callback(request):
    if request.method != 'POST':
        return HttpResponse('入力がおかしいです！！', status=405)

    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')

    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        return HttpResponseForbidden()
    except LineBotApiError:
        return HttpResponseBadRequest()

    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        message = ""
        if event.message.text in "名言教えて":
            quotes = list(Quote.objects.all())
            selected_quote = random.choice(quotes)
            message = selected_quote.text + "\n\n" + selected_quote.human
        else:
            message = "ワン！"

        text_send_message = TextSendMessage(text = message)
        line_bot_api.reply_message(
            event.reply_token,
            text_send_message
        )   
        
    return HttpResponse(status=200)