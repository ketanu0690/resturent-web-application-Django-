from django.http import HttpResponse 
from django.shortcuts import render
# from .cookies import *
from restro import settings
from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from.token import gentrate_token
from .pool import connection


def main(request):
    print("came to amin")
    return render(request,'main.html')
      

def intro(request):
    return render(request,'intro.html')


def register(request):
    print("came into resistration ")
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


def LOGIN_check(request):
    username = request.COOKIES.get('CookiesUsername')  
    password = request.COOKIES.get('CookiesPassword')
    
    # print(username,password)
    db,cmd = connection()
    q="select login_check from restro_db.user_table where username='{0}' and password ='{1}'".format(username,password)
    cmd.execute(q)
    user=cmd.fetchone()
    db.commit()
    print(user)
    
    if user[0] == "False":
        # print('idharr he a raha hai ')
        return render(request,'intro.html')
    if username is  None and password is None:
        return render(request,'intro.html')    
    else:    
        db,cmd = connection()
        q="select * from user_table where username='{0}' and password ='{1}'".format(username,password)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
        print(user)
        if user is not None:
            # print("came here")
            fname = user[1]
            # print(fname)
            db.close()

           
            return render(request,'main.html',{'fname':fname,'username':username,'password':password})

def login(request):
    # print("came into login ")
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']
        db,cmd = connection()
    
        q="select * from user_table where username='{0}' and password ='{1}'".format(username,password)
        
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
        print(user)
        
        if user is not None:
            # print("came here")
            db,cmd = connection()
            q="UPDATE user_table SET login_check = 'True' WHERE (username = '{0}');".format(username)
            cmd.execute(q)
            db.commit()
            fname = user[1]
            # print(fname)
            db.close()

           
            return render(request,'main.html',{'fname':fname,'username':username,'password':password})
        else:
            return render(request,'LOGIN.html',{'error':'Invalid Credentials'})

    return render(request,'LOGIN.html')

def logout(request, username):
    db,cmd = connection()
    q="update user_table set login_check='False' where username='{0}'".format(username)
    cmd.execute(q)
    db.commit()
    db.close()

    return render(request,'intro.html')
def scookie(request):  
    html = HttpResponse("<h1>Welcome to TechVidvan Employee Portal</h1>")
    html.set_cookie('TechVidvan', 'We are setting a cookie', max_age = None)
    return html
def gcookie(request):  
    tutorial  = request.COOKIES['java-tutorial']  
    return HttpResponse("java tutorials @: "+  tutorial);     

def activate(request, uidb64, token):

    try:
        print("came here")
        uid = force_text(urlsafe_base64_decode(uidb64))
        db,cmd = connection()
        q="select * from user_table where username='{0}'".format(uid)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
        # print(user)
        # print(user[0])
        # print("tokennnnnnnnnnnnnnnnnnn",gentrate_token.check_token(user[0],token))
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        # print("eeeeeeeeeeeeeeeeeeeeeeeerrorrrrrrrrrrrrr")
        user = None
    if user is not None and gentrate_token.check_token(user[0],token):
        print("came here")
        db,cmd = connection()
        q="UPDATE user_table SET login_check = 'True' WHERE (username = '{0}');".format(uid)
        cmd.execute(q)
        db.commit()
        db.close()
        # print("problem with cookies ")
        # value = "admin1"
        # setcookie(value)
        print("no problem with cookies ")
        return render(request,'main.html',{'success':'Account Activated','username':uid})
        # return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        # print("errorrrrrrrrrrrrrrrrrrrrrrrrrrrr")
        return HttpResponse('Activation link is invalid!')



def order(request):
    if request.method == 'POST':
        db,cmd = connection()
        q="select * from restro_db.order_table"
        cmd.execute(q)
        order=cmd.fetchall()
        db.commit()
        # print(order)
        db.close()
        return render(request,'order.html',{'order':order})
    return render(request,'order.html')

def MenuItems(request):
    if request.method == 'POST':
        db,cmd = connection()
        q="select * from restro_db.menu_table"
        cmd.execute(q)
        menu=cmd.fetchall()
        db.commit()
        # print(menu)
        db.close()
        return render(request,'menu.html',{'menu':menu})
    return render(request,'menu.html')    


    







