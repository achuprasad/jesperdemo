from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout

from jespapp.forms import PersonForm, DocumentForm
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
        context={}
        email = request.POST.get('email')
        password_value = request.POST.get('password')
        if not password_value or not email:
            context['password']='This field is required'
            return render(request, 'register.html',context)

        author, created = Person.objects.get_or_create(email=email)
        if created:
            print('status',created)
            author.set_password(password_value)
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
            user=Person.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return redirect('/dashboard/')
            else:
                context['passwordworng'] = "worng password"
                return render(request, 'login.html', context)
            # print('.......here')
        except:
            context={'error':'account doesnot exits'}
            return render(request,'login.html',context)
def logout_view(request):
    logout(request)
    return redirect('/login/')
class Dashboard(View):

    def get(self,request):
        context={}
        # if request.user.is_anonymous:
        #     context['showmodal']=True
        #     print(context['showmodal'])
        to = request.GET.get("to")

        context["to"] = to
        print(request.user,':::::::::::::::::::::::::::::::::::----request.user')
        return render(request,'dashborad.html',context)


class CommonPage(View):
    def get(self,request):
        return render(request,'common.html')


class DocumentView(View):
    def get(self,request):
        context={}
        print(request.GET.dict(),'.>>>>>>>>>>>>>>')

        if request.GET.get("q"):
            if request.user.is_anonymous:
                context['showmodal'] = True
                print(context['showmodal'])
            form=DocumentForm()
            context['form'] = form


        return render(request,'document.html',context)

    def post(self,request):
        context={}
        form=DocumentForm(request.POST)
        context = request.POST.dict()
        if form.is_valid():
            print(',,,,,1111')
            pass
        else:
            print('elseeeee')
            context['form'] = form
            return render(request,'document.html',context)