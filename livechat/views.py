from django.shortcuts import render,redirect
from .models import Room,Message
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def chat(request):
    rooms = Room.objects.all()
    return render(request, 'LiveChat/chat.html',{'rooms':rooms})
@login_required
def room(request, room):
    user = request.user
    room_details = Room.objects.get(name=room)
    rooms = Room.objects.all()
    return render(request, 'LiveChat/room.html', {'username': user.username, 'room': room, 'room_details': room_details,'rooms':rooms})

def checkview(request):
    room= request.POST['room_name']
    is_private = request.POST.get('is_private')
    room_code = request.POST['room_code']
    username = request.user.username
    #si algun objeto en el modelo Room tiene el nombre que conseguimos del request:
    if is_private :
        if Room.objects.filter(name=room,is_private=True,room_code=room_code).exists():
            add_owner = Room.objects.filter(name=room,is_private=True,room_code=room_code)
            add_owner.owner = request.user
            return redirect(room+'/?username='+username)
            
        else:
            new_room = Room.objects.create(name=room, is_private=True,room_code=room_code)
            new_room.save()
            new_room.owner.add(request.user)
            return redirect(room+ '/?username='+username)
    else:
        is_private = False
        if Room.objects.filter(name=room).exists():
            return redirect(room+'/?username='+username)
        else:
            new_room = Room.objects.create(name=room)
            new_room.save()
            return redirect(room+ '/?username='+username)


def send(request):
    message = request.POST['message']
    username = request.user.username
    room_id = request.POST['room_id']
    new_message = Message.objects.create(value=message,user= username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent succesfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room = room_details.id)
    return JsonResponse({"messages":list(messages.values())})

