from django.http import HttpResponse ,JsonResponse
from django.shortcuts import render,redirect
import json
from restro import settings
from django.core.mail import send_mail , EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from.token import gentrate_token
from .pool import connection


def main(request):
    # db,cmd = connection()
    # q="select * from menu"
    # MenuData = cmd.execute(q)    
    # db.commit()
    # print(MenuData)
    # return render(request,'main.html',{'MenuData':MenuData})
    response = redirect('/')
    return response
      

def intro(request):
    return render(request,'intro.html')


def register(request):
    # print("came into resistration ")
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
           

            return render(request,'GO_TO_EMAIL.html',{'success':'Registerd Successfully'})
            
    return render(request,'register.html')


def LOGIN_check(request):
# fetching cookies from user to auto login 
    db,cmd = connection()
    username = request.COOKIES.get('CookiesUsername')  
    password = request.COOKIES.get('CookiesPassword')
    
    #checking user has logout or not 
    q="select login_check from restro_db.user_table where username='{0}' and password ='{1}'".format(username,password)
    cmd.execute(q)
    user=cmd.fetchone()

    db.commit()
    
    if user[0] == "False":
        return render(request,'intro.html')
    if username is  None and password is None:
        return render(request,'intro.html')    
    else: 

        q="select * from user_table where username='{0}' and password ='{1}'".format(username,password)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
        

        if user is not None:
            fname = user[1]
            q="select * from menu"
            cmd.execute(q)    
            MenuData = cmd.fetchall()

            db.commit()
        
            db.close()
 
            return render(request,'main.html',{'fname':fname,'username':username,'password':password,'MenuData':MenuData})
           

def login(request):
    db,cmd = connection()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['pass']

        # checking user is present or not
        q="select * from user_table where username='{0}' and password ='{1}'".format(username,password)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
        
        if user is not None:
            # set login check to true
           
            q="UPDATE user_table SET login_check = 'True' WHERE (username = '{0}');".format(username)
            cmd.execute(q)
            db.commit()
            fname = user[1]
            # to fetch menu data
            q="select * from menu"
            MenuData = cmd.execute(q) 
            MenuData = cmd.fetchall()   
            db.commit()
            db.close()
            

            return render(request,'main.html',{'fname':fname,'username':username,'password':password,'MenuData':MenuData})
        else:
            return render(request,'LOGIN.html',{'error':'Invalid Credentials'})

    return render(request,'LOGIN.html')

def logout(request, username):
    db,cmd = connection()
    q="update user_table set login_check='False' where username='{0}'".format(username)
    cmd.execute(q)
    db.commit()
    db.close()

    response = redirect('/')
    return response

def activate(request, uidb64, token):
# activating the account on email check
    try:
        print("came here")
        uid = force_text(urlsafe_base64_decode(uidb64))
        db,cmd = connection()
        q="select * from user_table where username='{0}'".format(uid)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
       
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
      
        user = None
    if user is not None and gentrate_token.check_token(user[0],token):
        print("came here")
        db,cmd = connection()
        q="UPDATE user_table SET login_check = 'True' WHERE (username = '{0}');".format(uid)
        cmd.execute(q)
        db.commit()
        db.close()
    
        # print("no problem with cookies ")
        return render(request,'main.html',{'success':'Account Activated','username':uid})
      
    else:
     
        return HttpResponse('Activation link is invalid!')



def order(request, orderId):
    # to fetch data from order tabel and send to order.html
    if request.method == 'POST':
        db,cmd = connection()
        q="select * from restro_db.order_table"
        cmd.execute(q)
        order=cmd.fetchall()
        db.commit()
        db.close()
        return render(request,'order.html',{'order':order})

    return render(request,'AddReasturant/order.html',{'orderId':orderId})

def MenuItems(request):
    # to fetch data from menu tabel and send to menu.html
    if request.method == 'POST':
        db,cmd = connection()
        q="select * from restro_db.menu_table"
        cmd.execute(q)
        menu=cmd.fetchall()
        db.commit()
        db.close()
        return render(request,'menu.html',{'menu':menu})
    return render(request,'menu.html')    

def ViewProducts(request, orderId):
    return render(request,'ViewProduct.html',{'orderId':orderId})

def updatecart(request):
    data  = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    
    print("productId :",productId,"action :",action)
    
    return JsonResponse("updated item",safe=False)


def AddToCart(request):
    return render(request,'AddToCart.html')    

def CheckOut(request):
    return render(request,'CheckOut.html')    
    







