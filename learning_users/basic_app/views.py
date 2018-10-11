from django.shortcuts import render
from basic_app.forms import UserProfileInfoForm,UserForm

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
   return HttpResponse('Thank you')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

def register(request):
    registered = False
    if request.method=="POST":
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)
        #validation
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            #hashing the password
            user.set_password(user.password)
            user.save()

            #we cant save the profile pic in the database until it is there
            # we cant commit to it
            profile = profile_form.save(commit=False)
            # now to link this profile to the user
            profile.user = user
            # now if you get a FIles request
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered = True
        else:
            print(user_form.errors,profile_form.errors)
    #this might not be the http type of POST
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request,'basic_app/register.html',{'user_form':user_form,'profile_form':profile_form, 'registered':registered})

def user_login(request):
    if request.method =='POST':

       username = request.POST.get('username')
       password = request.POST.get('password')

       user = authenticate(username = username,password = password)

       if user:
           if user.is_active:
               login(request,user)
               return HttpResponseRedirect(reverse('index'))

           else:
               return HttpResponse("user id is inactive")
       else:
          return HttpResponse("we are sorry the username and the password did not match")
    else:
        return render(request,'basic_app/login.html',{})
