from django.shortcuts import render, redirect
from .models import Room, Message


def CreateRoom(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        room_name = request.POST.get('room')
        room = Room.objects.get_or_create(name=room_name)[0]
        return redirect("room", room_name=room_name, username=username)
    return render(request, 'index.html')

def MessageView(request, room_name, username):
    messages = Message.objects.filter(room__name=room_name)

    context = {
        "messages": messages,
        "user": username,
        "room_name": room_name
    }
    return render(request, "message.html", context)
