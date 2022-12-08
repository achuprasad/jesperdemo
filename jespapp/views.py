from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate

from jespapp.forms import PersonForm
from jespapp.models import Person


# Create your views here.

class LogView(View):

    def get(self,request):

        return render(request,'index.html')

    def post(self,request):
        context={}
        email=request.POST.get('email')
        if email:
            try:
                perosn_email=Person.objects.get(email=email)
                request.session['email']=perosn_email.email
                print(request.session['email'],'.>>>>>>>>>>>>')
                return redirect('/login/')
            except:
                context['errormessage']="Account doesn’t exist with the provided email. Please proceed with creating an account"

                return render(request,'index.html',context)

        return render(request,'index.html',context)


class Register(View):
    def get(self,request):

        return render(request,'register.html')
    def post(self,request):
        email = request.POST.get('email')
        password_value = request.POST.get('password')

        author, created = Person.objects.get_or_create(email=email)
        if created:
            print('status',created)
            author.password=password_value
            author.save()
            request.session['account_created']='Account is created please login'
            return redirect('/login/')
        message = "account already exits"
        return render(request, 'register.html', {'message': message})



class Login(View):
    def get(self,request):
        context={}

        # context['email']=request.session.get('email')
        # print(request.session.get('email'),"...............................1")
        if request.session.get('email'):
            context['email'] = request.session.get('email')
            del request.session['email']
        else:
            context['email'] = ''
        if request.session.get('account_created'):
            context['account_message']=request.session.get('account_created')
            # context['email'] = request.session.get('email')
            del request.session['account_created']


        return render(request,'login.html',context)
    def post(self,request):
        context={}
        email=request.POST.get('email')
        print(email,'.<<<<<email>>>>>')
        password=request.POST.get('password')
        print(password,'.<<<<<<password>>>>>>>')
        try:
            a=Person.objects.get(email=email)
            # print('.......here')
        except:
            context={'error':'account doesnot exits'}
            return render(request,'login.html',context)

        if a:
            print(',,,,,,hereqqiammmmmm')
            user = Person.objects.get(email=email)
            print(user,'.,,,,,,,,,>>>>>>>>')
            user.check_password(password)
            print(user.check_password(password),'..................2121')
            login(request, user)
            return redirect('/dashboard/')
        # user = authenticate(email=email,password=password)
        # print(user,'..........here')
        # if user is not None:
        #     print('........................here11111')
        #     request.session['email'] = ''
        #     login(request, user)
        #     print('enter.....')
        #     return redirect('/dashboard/')

        return render(request,'login.html',context)

class Dashboard(View):

    def get(self,request):
        print(request.user,':::::::::::::::::::::::::::::::::::----request.user')
        return render(request,'dashborad.html')