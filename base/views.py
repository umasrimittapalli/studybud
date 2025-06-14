from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
# from django.contrib.auth.forms import UserCreationForm
from .models import Room,Topic,Message,User
from .forms import RoomForm,UserForm, MyUserCreationForm

from django.contrib.auth.decorators import login_required




# Create your views here.


# Rooms=[
#     {"id":1, 'name':'lets learn python!'},
#     {"id":2, 'name':'Design with me'},
#     {"id":3, 'name':'lets learn django!'},
# ]

def loginPage(request):
   page="login"
   if request.user.is_authenticated:
      return redirect('home')
   
   if request.method=='POST':
      email=request.POST.get('email').lower()
      password=request.POST.get('password')

      try:
         user =User.objects.get(email=email)
      except:
         messages.error(request,'User does not exit')

      user = authenticate(request,email=email,password=password)
      
      if user is not None:
         login(request,user)
         return redirect('home')
      else:
         messages.error(request,'Username OR password does not exit ')

   context={'page':page}
   return render(request,'base/login_register.html',context)

def logoutUser(request):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
   logout(request)
   return redirect('home')


def registerpage(request):                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
   #page='register'
   form =MyUserCreationForm()
   if request.method =='POST':
       form =MyUserCreationForm(request.POST)
       if form .is_valid():
          user=form.save(commit=False)
          user.username == user.username.lower()
          user.save()
          login(request,user)
          return redirect('home')
       else:
          messages.error(request,'An error occured during registertion')
          
   return render(request,'base/login_register.html',{'form':form})






def home(request):
    q= request.GET.get('q') if request.GET.get('q') != None else ''
   #  Rooms=Room.objects.all()
    Rooms=Room.objects.filter(
       Q(topic__name__icontains=q) |
       Q(name__icontains=q) |
       Q(descritption__icontains=q) 
       
    )
     
   
    Topics=Topic.objects.all()[0:5]
    room_count=Rooms.count()

   #  room_messages=Message.objects.all()

    room_messages=Message.objects.filter(
       Q(room__topic__name__icontains=q) 
                                         )
    context={'rooms':Rooms ,'topics':Topics ,'room_count':room_count ,
             'room_messages':room_messages}
    return render(request,"base/home.html", context)


def room(request,pk):
    # room=None
    # for k in Rooms:
    #     if k['id'] == int(pk):
    #         room =k

    room=Room.objects.get(id=pk)
    room_messages =room.message_set.all().order_by('-created')
    partcipants=room.participants.all()
    if request.method == "POST":
       message = Message.objects.create(
       user=request.user,
       room=room,
       body = request.POST.get('body')

       )
       room.participants.add(request.user)
       return redirect('room', pk=room.id)


    context1={'rooms':room,'room_messages':room_messages,'partcipants':partcipants}
    return render(request,"base/room.html",context1)


def userprofile(request,pk):
  user =User.objects.get(id=pk)
  rooms=user.room_set.all()
  room_messages=user.message_set.all()
  topics=Topic.objects.all()
  context={'user':user,'rooms': rooms,'room_messages':room_messages,
           'topics':topics}
  return render(request,'base/profile.html' ,context)












@login_required(login_url='/login')

def createRoom(request):
 form= RoomForm() 
 topics=Topic.objects.all()
 if request.method =='POST':
    topic_name= request.POST.get('topic')
    topic,created =Topic.objects.get_or_create(name=topic_name)
    
    Room.objects.create(
       host=request.user,
       topic=topic,
       name=request.POST.get('name'),
       descritption=request.POST.get('descritption'),
    )
    return redirect('home')

 con={'form':form,'topics':topics}
 return render(request,"base/room_form.html",con)

@login_required(login_url='/login')
def updateRoom(request,pk):
   room =Room.objects.get(id=pk)
   form=RoomForm(instance=room) 
   topics=Topic.objects.all() 
   if request.user != room.host:
      return HttpResponse("Sorry !! your are not allowed to this room")
    
   if request.method == 'POST':
      topic_name= request.POST.get('topic')
      topic,created =Topic.objects.get_or_create(name=topic_name)
      room.name= request.POST.get('name')
      room.topic= topic
      room.descritption=request.POST.get('descritption')
      room.save()
      return redirect('home')

   context={'form':form,'topics':topics,'room':room}
   return render(request,"base/room_form.html",context) 


@login_required(login_url='/login')
def deleteRoom(request,pk):
    room =Room.objects.get(id=pk)
    if request.user != room.host:
      return HttpResponse("Sorry !! your are not allowed to this room")
    if request.method=='POST':
       room.delete()
       return redirect('home')
    return render(request,"base/delete.html",{'obj':room}) 


@login_required(login_url='/login')
def deleteMessage(request,pk):
    message =Message.objects.get(id=pk)
    if request.user != message.user:
      return HttpResponse("Sorry !! your are not allowed to this room")
    if request.method=='POST':
       message.delete()
       return redirect('home')
    return render(request,"base/delete.html",{'obj':message}) 



@login_required(login_url='/login')
def updateuser(request):
   user =request.user
   form=UserForm(instance=user)
   if request.method=='POST':
      form=UserForm(request.POST,request.FILES,instance=user)
      if form.is_valid():
         form.save()
      return  redirect ('user-profile',pk=user.id)

   return render(request,'base/update-user.html',{'form':form})

@login_required(login_url='/login')
def topicsPage(request):
   q= request.GET.get('q') if request.GET.get('q') != None else ''
   topics = Topic.objects.filter(name__icontains=q)
   return render(request,'base/topics.html',{'topics':topics})
 

@login_required(login_url='/login')
def activityPage(request):
   room_messages=Message.objects.all
   return render(request,'base/activity.html',{'room_messages':room_messages})



