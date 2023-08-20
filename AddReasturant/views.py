from logging import error
from django.http import HttpResponse 
from django.shortcuts import redirect, render
from restro import settings
from django.core.mail import send_mail , EmailMessage , EmailMultiAlternatives
from django.template.loader import get_template
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from restro.token import gentrate_token
from restro.pool import connection


def AddReasturant(request):
    return render(request, 'AddReasturant/AddReasturant.html')

def Addlogin(request):
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
            cmd.execute(q) 
            MenuData = cmd.fetchall()   
            db.commit()

            q="select quantity from order_item "
            cmd.execute(q)
            order_item = cmd.fetchall()
            db.commit()
            sum_quantity = 0
            for i in order_item:
                sum_quantity = sum_quantity + i[0]
            # print(sum_quantity)
            db.close()
            
            return redirect('/Dashboard')   
            # return render(request,'main.html',{'fname':fname,'username':username,'password':password,'MenuData':MenuData,'sum_quantity':sum_quantity})
        else:
            return render(request,'LOGIN.html',{'error':'Invalid Credentials'})

    return render(request,'AddReasturant/LOGIN.html')


def Addregister(request):
    
    if request.method == 'POST':
        username = request.POST['username']
        phone = request.POST['phone']
        city = request.POST['city']
        address = request.POST['address']
        rasturantName = request.POST['rasturantName']
        fullname = request.POST['fullname']
        email = request.POST['email']
        password = request.POST['pass']
        confirmpassword = request.POST['c_pass']
        user_login_check = False
        if phone is not None:
            if len(phone) != 10:
                return render(request,'AddReasturant/LOGIN.html',{'error':'Phone Number is not valid'})
        if email is not None:
            if '@' not in email:
                return render(request,'AddReasturant/LOGIN.html',{'error':'Email is not valid'})
        if city is not None:
            if len(city) < 3:
                return render(request,'AddReasturant/LOGIN.html',{'error':'City is not valid'})
        if address is not None:
            if len(address) < 3:
                return render(request,'AddReasturant/LOGIN.html',{'error':'Address is not valid'})
        if rasturantName is not None:
            if len(rasturantName) < 3:
                return render(request,'AddReasturant/LOGIN.html',{'error':'Rasturant Name is not valid'})
        if fullname is not None:
            if len(fullname) < 3:
                return render(request,'AddReasturant/LOGIN.html',{'error':'Full Name is not valid'})
        if username is not None:
            if len(username) < 3:
                return render(request,'AddReasturant/LOGIN.html',{'error':'Username is not valid'})



        db,cmd = connection()
        q="select * from restaurant_user_table where username='{0}' or email ='{1}'".format(username,email)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()

        if user is not None:
            return render(request,'AddReasturant/LOGIN.html',{'error':'Username or email  already exist'})
    
        if len(username) < 6:
            return render(request,'AddReasturant/LOGIN.html',{'error':'Username should be atleast 10 characters'})

        if not username.isalnum():
            return render(request,'AddReasturant/LOGIN.html',{'error':'Username should be alpha numeric  only'})            
        
        if password != confirmpassword:
            return render(request,'AddReasturant/LOGIN.html',{'error':'Password and Confirm Password does not match'})  
    
        else:
            db,cmd = connection()
            q="INSERT INTO restro_db.restaurant_user_table (username, password, email,phone_number,user_login_check,address,full_name,restaurant_name,city) VALUES ('{0}','{1}' ,'{2}','{3}','{4}','{5}','{6}','{7}','{8}');".format(username,password,email,phone,user_login_check,address,fullname,rasturantName,city)
            cmd.execute(q)
            db.commit()
            db.close()

            # welcome email message 
            subject = 'Welcome Email From Restro'
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            message = EmailMultiAlternatives(subject, '', from_email, to_list)
            html_template = get_template('email_template.html')
            message.attach_alternative(html_template.render(), "text/html")
            message.send()

            #email address confirmation message

            current_site = get_current_site(request)
            subject = 'Email Confirmation'
            from_email = settings.EMAIL_HOST_USER
            to_list = [email]
            content_data = {
                'name':fullname,
                'domain':current_site.domain,
                'uid':username,
                'token':gentrate_token.make_token(username)
                }
            print(content_data['uid'])
            message = EmailMultiAlternatives(subject, '', from_email, to_list)
            html_template = get_template('AddReasturant/Add_email_confirmation_message.html').render(content_data)
            message.attach_alternative(html_template, "text/html")
            message.send()

            # phone oTP validation message
            subject = 'Phone OTP'




            return render(request,'GO_TO_EMAIL.html',{'success':'Registerd Successfully'})
            
    return render(request,'AddReasturant/register.html')
    

def Addactivate(request, uidb64, token):
    db,cmd = connection()
    q="UPDATE restaurant_user_table SET user_login_check = 'True' WHERE (username = '{0}');".format(uidb64)
    cmd.execute(q)
    db.commit()
    db.close()
    return redirect('/Dashboard')

def Dashboard(request):
    return render(request,'AddReasturant/Dashboard.html')

def Insertmenu(request):

    if request.method == 'POST':
        dish_name = request.POST['dish_name']
        dish_description = request.POST['dish_description']
        dish_image = request.FILES['dish_image']
        dish_price = request.POST['dish_price']
        dish_category = request.POST['dish_category']

        db,cmd=connection()
        q=""" INSERT INTO menu(name, description,image,price,category) VALUES (%s,%s,%s,%s,%s)"""
        
        cmd.execute(q,(dish_name,dish_description,dish_image.name,dish_price,dish_category))
        db.commit()
        db.close()

        f=open("D:/HTML--CSS/project/restro/resturent-web-application-Django-/asset/"+dish_image.name,"wb")
        
        for chunk in dish_image.chunks():
            f.write(chunk)
        
        f.close()
        return HttpResponse('Data is  saved')

    return HttpResponse('Data is  not saved')