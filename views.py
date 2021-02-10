from django.shortcuts import render, redirect
from .models import User
from .models import Message
from .models import Comment
from django.contrib import messages
import bcrypt

hash1 = bcrypt.hashpw('test'.encode(), bcrypt.gensalt())

def index(request):

    if "first_name" not in request.session:
        request.session['first_name'] = ""
        request.session['id'] = ""

    return render(request, 'wall_app/index.html')

def login(request):

    return render(request, 'wall_app/login.html')

def register(request):

    return render(request, 'wall_app/register.html')

def success(request):

    return render(request, 'wall_app/success.html')

def show(request):

    context = {
        "messages": Message.objects.all(),
        "comments": Comment.objects.all(),
        "users": User.objects.all()
    }

    return render(request, 'wall_app/thewall.html', context)

def logout(request):

    return render(request, "wall_app/logout.html")

def logoutofthewall(request):
    request.session.clear()
    return redirect('/')


def signin(request):
    if (request.method == "POST") & (request.POST['hidden'] == "Login"):
        errors = User.objects.login_validator(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/login')

        user = User.objects.get(email=request.POST['LEmail'])
        if bcrypt.checkpw(request.POST['LPassword'].encode(), user.pw.encode()):
            print(user.pw)
            active = User.objects.get(email=request.POST['LEmail'])
            messages.success(request, "You're logged in!!")
            request.session['first_name'] = active.first_name
            request.session['id'] = active.id
            return redirect('/success')
        else:
            errors['lpw'] = "That password or e-mail did not match"
            messages.error(request, errors['lpw'])
            return redirect('/login')


def create(request):
    if (request.method == "POST") & (request.POST['hidden'] == "Register"):
        errors = User.objects.registration_validator(request.POST)

        if len(errors):
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/register')
        else:
            newFirst = request.POST['f_name']
            newLast = request.POST['l_name']
            newEmail = request.POST['email']
            newPw = request.POST['pw']
            if newPw == request.POST['cpw']:
                encryptedPW = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt())
            b = User(first_name=newFirst, last_name=newLast, email=newEmail, pw=encryptedPW)
            b.save()
            messages.success(request, "Successfully registered!")
            request.session["first_name"] = newFirst
            request.session['id'] = b.id
            return redirect('/success')

def message(request):
    if request.method == "POST":
        newMessage = request.POST['messageBox']
        author = request.session['id']
        print(author)
        Message.objects.create(newmessage=newMessage, user=User.objects.get(id=author))
    return redirect('/thewall')

def comment(request):
    if request.method == "POST":
        newComment = request.POST['commentBox']
        messageid = Message.objects.get(id=request.POST['messageID'])
        commentor = request.session['id']
        Comment.objects.create(newcomment=newComment, user=User.objects.get(id=commentor), message=messageid)
        print(Comment.objects.all().values())
        print(commentor)
        print(User.objects.get(id=4).__dict__)
    return redirect('/thewall')

def delete(request):
    if request.method == "POST":
        Comment.objects.get(id=request.POST['commentID']).delete()
    return redirect('/thewall')

def remove(request):
    if request.method == "POST":
        Message.objects.get(id=request.POST['messageID']).delete()
    return redirect('/thewall')