from django.shortcuts import render
from .models import Room
from django.conf import settings
from django.http import JsonResponse
from twilio.jwt.access_token import AccessToken
from twilio.jwt.access_token.grants import ChatGrant


def new_user(request):
    return render(request, 'chat/form.html')


def all_rooms(request):
    global username
    if request.method == 'POST':
        username = request.POST.get('textfield', None)
    else:
        username = 'Jeff'
    rooms = Room.objects.all()
    return render(request, 'chat/index.html', {'rooms': rooms})


def room_detail(request, slug):
    room = Room.objects.get(slug=slug)
    return render(request, 'chat/room_detail.html', {'room': room})


def token(request):
    identity = request.GET.get('id', username)
    device_id = request.GET.get('device', 'default')

    account_sid = settings.TWILIO_ACCOUNT_SID
    api_key = settings.TWILIO_API_KEY
    api_secret = settings.TWILIO_API_SECRET
    chat_service_sid = settings.TWILIO_CHAT_SERVICE_SID

    token = AccessToken(account_sid,
                        api_key,
                        api_secret,
                        identity=identity)

    endpoint = "eQualityChatRoom:{0}:{1}".format(identity, device_id)

    if chat_service_sid:
        chat_grant = ChatGrant(endpoint_id=endpoint,
                               service_sid=chat_service_sid)
        token.add_grant(chat_grant)

    response = {'identity': identity,
                'token': token.to_jwt().decode('utf-8')}

    return JsonResponse(response)
