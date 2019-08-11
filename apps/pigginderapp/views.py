from __future__ import unicode_literals
from django.core.files import File
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from datetime import datetime
from .models import User, Relationship, Message
from .forms import UploadFileForm
import bcrypt

def index(request):
    return render(request, 'pigginderapp/index.html')

def register(request):
    return render(request, 'pigginderapp/register.html')

def register_processing(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/register')
        
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        gender = request.POST['gender']
        breed_type = request.POST['breed_type']
        password = bcrypt.hashpw(request.POST['password'].encode(),bcrypt.gensalt())
        User.objects.create(first_name=first_name, last_name=last_name, email=email, gender=gender, breed_type = breed_type, password=password)

        user = User.objects.get(email=email)
        request.session['logged_in'] = True
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['gender'] = user.gender
        request.session['breed_type'] = user.breed_type
        request.session['email'] = user.email
        request.session['user_id'] = user.id
        return redirect('/last_confirmation')

def login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/register')
    else:
        email = request.POST['input_email']
        password = bcrypt.hashpw(request.POST['input_password'].encode(),bcrypt.gensalt())
        user = User.objects.get(email=email)
        request.session['logged_in'] = True
        request.session['first_name'] = user.first_name
        request.session['last_name'] = user.last_name
        request.session['email'] = user.email
        request.session['user_id'] = user.id
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    active_user= User.objects.get(id=request.session["user_id"])
    likes = Relationship.objects.filter(pigOne=active_user, accepted=0) | Relationship.objects.filter(pigOne=active_user, accepted=1) 
    likingbacks = Relationship.objects.filter(pigTwo=active_user, accepted=1)
    likes_count = len(likes) + len(likingbacks)

    liked = Relationship.objects.filter(pigTwo=active_user, accepted=0) | Relationship.objects.filter(pigTwo=active_user, accepted=1) 
    likedback = Relationship.objects.filter(pigOne=active_user, accepted=1)
    liked_count = len(liked) + len(likedback)

    messages = Message.objects.filter(receiver=active_user)

    context = {
        "active_user": User.objects.get(id=request.session["user_id"]),
        "users": User.objects.all(),
        "likes_count": likes_count,
        "liked_count": liked_count,
        "messages": messages,
    }
    return render(request, 'pigginderapp/dashboard.html', context)

def last_confirmation(request):
    form = UploadFileForm()
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "form": form,
    }
    return render(request, 'pigginderapp/last_confirmation.html', context)

def last_info_processing(request):
    request.session['logged_in'] = True
  
    print(request.POST)
    errors = User.objects.last_validator(request.POST)
    print(errors)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/last_confirmation')
        
    else:
        user=User.objects.get(id=request.session['user_id'])
        form = UploadFileForm(request.FILES)
        user.profile_picture = request.FILES['file']
        user.description = request.POST['description']
        user.relationship_goal = request.POST['relationship_goal']
        user.save()
        return redirect('/dashboard')

def profile(request):
    form = UploadFileForm()
    context = {
        "user": User.objects.get(id=request.session["user_id"]),
        "form": form,
    }
    return render(request, 'pigginderapp/profile.html', context)

def editing_profile(request):
    request.session['logged_in'] = True
  
    errors = User.objects.last_validator(request.POST)
    if len(errors) > 0:
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect('/profile')

    else:
        user=User.objects.get(id=request.session['user_id'])
        form = UploadFileForm(request.FILES)
        user.profile_picture = request.FILES['file']
        user.description = request.POST['description']
        user.relationship_goal = request.POST['relationship_goal']
        user.save()
        return redirect('/dashboard')

def pick(request, piggie_id):
    piggieTwo = User.objects.get(id=piggie_id)
    context = {
        "piggieOne": User.objects.get(id=request.session['user_id']),
        "piggieTwo": User.objects.get(id=piggie_id)
    }
    return render(request, 'pigginderapp/pick.html', context)

def bye(request, piggie_id):
    piggieOne= User.objects.get(id=request.session['user_id'])
    piggieTwo = User.objects.get(id=piggie_id)
    relationship = Relationship.objects.filter(pigOne=piggieOne, pigTwo=piggieTwo)

    if len(relationship) == 0:
        Relationship.objects.create(pigOne=piggieOne, pigTwo=piggieTwo, accepted=2)

    else:
        relationship[0].accepted = 2
        relationship[0].save()
    return redirect('/dashboard')

def like(request, piggie_id):
    piggieOne= User.objects.get(id=request.session['user_id'])
    piggieTwo = User.objects.get(id=piggie_id)
    relationship = Relationship.objects.filter(pigOne=piggieOne, pigTwo=piggieTwo)

    if len(relationship) > 0:
        relationship[0].accepted = 0
        relationship[0].save()
        return redirect('/dashboard')

    else:
        Relationship.objects.create(pigOne = piggieOne, pigTwo = piggieTwo, accepted=0)
        return redirect('/dashboard')

def matched_result(request):
    active_user= User.objects.get(id=request.session["user_id"])
    piggieOne= User.objects.get(id=request.session['user_id'])
    likes = Relationship.objects.filter(pigOne=active_user, accepted=0)
    liked = Relationship.objects.filter(pigTwo=active_user, accepted=0)

    context = {
        "active_user": User.objects.get(id=request.session["user_id"]),
        "users": User.objects.all(),
        "likes" : likes,
        "liked" : liked,
        "piggieOne": User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'pigginderapp/matchinfo.html', context)

def matched_with(request, piggie_id): 
    piggieOne= User.objects.get(id=request.session['user_id'])
    piggieTwo = User.objects.get(id=piggie_id)
    context = {
        "piggieOne": User.objects.get(id=request.session['user_id']),
        "piggieTwo": User.objects.get(id=piggie_id)
    }
    return render(request, 'pigginderapp/match.html', context)

def friendzone(request, piggie_id):
    piggieOne= User.objects.get(id=request.session['user_id'])
    piggieTwo = User.objects.get(id=piggie_id)
    # likes = Relationship.objects.filter(pigOne=piggieOne)
    # liked = Relationship.objects.filter(pigTwo=piggieOne)
    relationship = Relationship.objects.get(pigOne = piggieTwo, pigTwo = piggieOne)
    relationship.accepted=2
    relationship.save()
    return redirect('/matched_result')

def likingback(request, piggie_id):
    piggieOne= User.objects.get(id=request.session['user_id'])
    piggieTwo = User.objects.get(id=piggie_id)
    relationship = Relationship.objects.get(pigOne = piggieTwo, pigTwo = piggieOne)
    relationship.accepted = 1
    relationship.save()
    return redirect('/matched_with/' + piggie_id)

def message(request, piggie_id): 
    context = {
        "piggieOne": User.objects.get(id=request.session['user_id']),
        "piggieTwo": User.objects.get(id=piggie_id)
    }
    return render(request, 'pigginderapp/message.html', context)

def messaging (request, piggie_id): 
    errors = Message.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/message/'+ piggie_id)
    else:
        piggieOne= User.objects.get(id=request.session['user_id'])
        piggieTwo = User.objects.get(id=piggie_id)
        Message.objects.create(message=request.POST['message'], sender=piggieOne, receiver=piggieTwo)
        return redirect("/dashboard")

def message_page(request, piggie_id):
    piggieOne= User.objects.get(id=request.session['user_id'])
    piggieTwo = User.objects.get(id=piggie_id)
    messages = Message.objects.filter(sender=piggieOne, receiver=piggieTwo) | Message.objects.filter(sender=piggieTwo, receiver=piggieOne) 
    ordered_message = messages.order_by("created_at")
    context = {
        "piggieOne": User.objects.get(id=request.session['user_id']),
        "piggieTwo": User.objects.get(id=piggie_id),
        "messages": ordered_message
    }
    return render(request, 'pigginderapp/message_page.html', context)

def messagingback(request, piggie_id):
    errors = Message.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/message_page/'+ piggie_id)
    else:
        piggieOne= User.objects.get(id=request.session['user_id'])
        piggieTwo = User.objects.get(id=piggie_id)
        Message.objects.create(message=request.POST['message'], sender=piggieOne, receiver=piggieTwo)
        return redirect("/dashboard")



