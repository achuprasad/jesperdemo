from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate, logout
from jespapp.forms import PersonForm, DocumentForm, DocumentForm1
from jespapp.models import Person, Documents
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
#convert pdf
import pdfkit
import os
import glob
from django.template.loader import get_template
from django.core.mail import EmailMessage



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
                return redirect('/common/')
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
        if request.session.get('emailsend'):
            print('..............email successs message')
            context['emailsend'] = request.session.get('emailsend')
            del request.session['emailsend']
        to = request.GET.get("to")

        context["to"] = to
        print(request.user,':::::::::::::::::::::::::::::::::::----request.user')
        return render(request,'dashborad.html',context)


class CommonPage(View):
    def get(self,request):
        return render(request,'common.html')


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    # filename = 'files/'
    list_of_files = glob.glob('files/*')  # * means all i------f need specific format then *.csv
    latest_file = max(list_of_files, key=os.path.getctime).split(".")[0]
    print("latest_file",latest_file)
    next_file_name = f"files/transcation{int(latest_file[17:]) + 1}.pdf"
    print("next_file_name", next_file_name)
    # latest_file_name = f_name.
    # name="transcation.pdf"
    # file=getUniquePath(filename,name)
    pdf = pdfkit.from_string(html, next_file_name)
    return next_file_name

class DocumentView(View):
    def get(self,request):
        context={}
        print(request.GET.dict(),'.>>>>>>>>>>>>>>')

        if request.GET.get("q") == "CA1":
            if request.user.is_anonymous:
                context['showmodal'] = True
                print(context['showmodal'])
            form=DocumentForm()
            context['form'] = form
        elif request.GET.get("q") == "CA2":
            if request.user.is_anonymous:
                context['showmodal'] = True
                print(context['showmodal'])
            form1=DocumentForm1()
            context['form1'] = form1
        else:
             context['docmessage']="New update will be coming soon"

        return render(request,'document.html',context)

    def post(self,request):
        context={}
        form=DocumentForm(request.POST)
        form1=DocumentForm1(request.POST)
        print('request.POST.get("category")>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>',request.POST.get("category"))
        context = request.POST.dict()
        if form.is_valid():
            doc=Documents.objects.create(firstname=request.POST.get("firstname"),
                                         middlename=request.POST.get("middlename"),
                                         lastname=request.POST.get("lastname"),
                                         address=request.POST.get("address"),
                                         pincode=request.POST.get("pincode"),
                                         type=request.POST.get("category"),
                                         created_by=request.user
                                         )
            doc.save()

            subject = 'welcome to PDF world'
            message = f'Hi {doc.firstname}, thank you for creating document.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [doc.created_by, ]
            # recipient_list = ["achuprasad@codesvera.com",]
            context={'firstname':doc.firstname,'lastname':doc.lastname,'pincode':doc.pincode}

            # template=render_to_string('email.html',context)
            pdf = render_to_pdf('email.html', context)
            print(pdf,'>>>>>>>>>>>>>>>>>>',type(pdf))
            # send_mail(subject, message, email_from, recipient_list,html_message=template)
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.attach_file(pdf)
            email.send()
            request.session['emailsend'] = "email send successfully"
            return redirect("/dashboard/")
        elif form1.is_valid():
            doc=Documents.objects.create(firstname=request.POST.get("firstname"),
                                         middlename=request.POST.get("middlename"),
                                         lastname=request.POST.get("lastname"),
                                         address=request.POST.get("address"),
                                         mobile=request.POST.get("mobile"),
                                         type=request.POST.get("category"),
                                         created_by=request.user)
            doc.save()
            subject = 'welcome to PDF world'
            message = f'Hi {doc.firstname}, thank you for creating document.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [doc.created_by, ]
            context = {'firstname': doc.firstname, 'lastname': doc.lastname, 'mobile': doc.mobile}
            # template=render_to_string('email.html',context)
            pdf = render_to_pdf('email.html', context)
            print(pdf, '>>>>>>>>>>>>>>>>>>', type(pdf))
            # send_mail(subject, message, email_from, recipient_list,html_message=template)
            email = EmailMessage(subject, message, email_from, recipient_list)
            email.attach_file(pdf)
            email.send()
            request.session['emailsend'] = "email send successfully"
            return redirect("/dashboard/")
        else:
            if not form.is_valid():
                context['form'] = form
            else:
                context['form1'] = form1
                print("context['form1']................", context['form1'])
            return render(request,'document.html',context)





















































































# # testing jespers html
#
# var as = window.location.href.split('?')[0];
# console.log("...........as", as );
# window.location.replace( as );
#
#
#
# replacing
# var
# currentUrl = $(location).attr('href');
# console.log(">.........", currentUrl)
# var
# url = new
# URL(currentUrl);
#
# url.searchParams.set('to', 'mode-two'); // setting
# your
# param
#
# var
# newUrl = url.href;
# window.location.replace(newUrl);
#
# console.log(newUrl);

