from django.http import HttpResponse 
from django.shortcuts import render
# from .cookies import *
from restro import settings
from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from restro.token import gentrate_token
from restro.pool import connection

# Create your views here.

def AddReasturant(request):
    return render(request, 'AddReasturant/AddReasturant.html')


def AddReasturantlogin(request):
        return render(request, 'AddReasturant/LOGIN.html')



def AddReasturantregister(request):
        return render(request, 'AddReasturant/register.html')

def Addlogin(request):
    pass

def Addregister(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass']
        confirmpassword = request.POST['c_pass']
        login_check = False

        db,cmd = connection()
        q="select * from user_table where username='{0}' or email ='{1}'".format(username,email)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
        if user is not None:
            return render(request,'register.html',{'error':'Username or email  already exist'})
    
        if len(username) < 6:
            return render(request,'register.html',{'error':'Username should be atleast 10 characters'})

        if not username.isalnum():
            return render(request,'register.html',{'error':'Username should be alpha numeric  only'})            
        
        if password != confirmpassword:
            return render(request,'register.html',{'error':'Password and Confirm Password does not match'})  
    
        else:
            db,cmd = connection()
            q="INSERT INTO restro_db.user_table (username, first_name, last_name, password, email,login_check) VALUES ('{0}','{1}' ,'{2}','{3}','{4}','{5}');".format(username,firstname,lastname,password,email,login_check)
            cmd.execute(q)
            db.commit()
            db.close()

            # welcome email message 
            subject = 'Welcome  Email From Restro'
            message = 'Hello '+firstname+'\n\n'+' Welcome to Restro '+'\n\n'+' Thank you for registering with us ....... '+'  we have sent you a confirmation email ..'+'thanking you \n\n from ketan upadhyay'+'\n\n'+' Please click on the link to activate your account  '
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            send_mail(subject,message,from_email,to_list,fail_silently=True)

            #email address confirmation message

            current_site = get_current_site(request)
            subject = 'Email Confirmation'
            # message = 'Hello'+firstname+'\n\n'+'Thank you for registering with us'+'\n\n'+'Please click on the link to activate your account'
            message2= render_to_string('email_confirmation_message.html',{
                'name':firstname,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(username)),
                'token':gentrate_token.make_token(username),

            })
            
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            email = EmailMessage(subject,message2,from_email,to_list)
            email.fail_silently=True
            email.send()
            # send_mail(subject,message,from_email,to_list,fail_silently=True)

            return render(request,'GO_TO_EMAIL.html',{'success':'Registerd Successfully'})
            
    return render(request,'register.html')
    


def Insertmenu(request):

    if request.method == 'POST':
        dish_name = request.POST['dish_name']
        dish_description = request.POST['dish_description']
        dish_image = request.FILES['dish_image']
        dish_price = request.POST['dish_price']
        dish_category = request.POST['dish_category']

        
        db,cmd=connection()
        q=""" INSERT INTO menu
                          (name, description,image,price,category) VALUES (%s,%s,%s,%s,%s)"""
        
        cmd.execute(q,(dish_name,dish_description,dish_image.name,dish_price,dish_category))
        db.commit()
        db.close()

        f=open("D:/HTML--CSS/project/restro/resturent-web-application-Django-/asset/"+dish_image.name,"wb")
        
        for chunk in dish_image.chunks():
            f.write(chunk)
          
        f.close()
        return HttpResponse('Data is  saved')

    return HttpResponse('Data is  not saved')