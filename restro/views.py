from datetime import datetime
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
    response = redirect('/')
    return response
      

def intro(request):
    return render(request,'intro.html')


def register(request):
    # print("came into resistration ")
    db,cmd = connection()
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['pass']
        confirmpassword = request.POST['c_pass']
        login_check = False
        uid =urlsafe_base64_encode(force_bytes(username))
        city= request.COOKIES.get('CookiesCity') 

        
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
            # q="INSERT INTO restro_db.user_table (uid, username, first_name, last_name, password, email, login_check, city`) VALUES ('yure', 'hhhj', 'jhvkh', 'hkjh', '78', 'ketanup@gm.com', 'false', 'gwal');"
            q="INSERT INTO restro_db.user_table (uid,username,first_name, last_name, password, email,login_check,city) VALUES ('{0}','{1}' ,'{2}','{3}','{4}','{5}','{6}','{7}');".format(uid,username,firstname,lastname,password,email,login_check,city)
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

            q="select quantity from order_item "
            cmd.execute(q)
            order_item = cmd.fetchall()
            db.commit()
            # to find sum of quantity of all order items
            sum_quantity = 0
            for i in order_item:
                sum_quantity = sum_quantity + i[0]
            print(sum_quantity)
    


            db.close()
 
            return render(request,'main.html',{'fname':fname,'username':username,'password':password,'MenuData':MenuData,'sum_quantity':sum_quantity})
           

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
            

            return render(request,'main.html',{'fname':fname,'username':username,'password':password,'MenuData':MenuData,'sum_quantity':sum_quantity})
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
        # print("came here")
        uid = force_text(urlsafe_base64_decode(uidb64))
        db,cmd = connection()
        q="select * from user_table where username='{0}'".format(uid)
        cmd.execute(q)
        user=cmd.fetchone()
        db.commit()
       
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
      
        user = None
    if user is not None and gentrate_token.check_token(user[0],token):
        # print("came here")
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
    # this is comming from adimin ppage 
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



def AddToCart(request, username):
    db,cmd = connection()
    q="select uid from user_table where username='{0}'".format(username)
    cmd.execute(q)
    uid = cmd.fetchall()
    db.commit()
    
    q2="select order_id from restro_db.order where uid='{0}'".format(uid[0][0])
    cmd.execute(q2)
    order_id = cmd.fetchall()
    db.commit()

    q3="select menu_id, quantity from restro_db.order_item where order_id={0}".format(order_id[0][0])
    cmd.execute(q3)
    order_item = cmd.fetchall()
    db.commit()

    menu_item = []
    for i in order_item:
        q4="select * from restro_db.menu where menu_id={0}".format(i[0])
        cmd.execute(q4)
        menu_item.append(cmd.fetchall())
        db.commit()
    
    quantity = []
    for x in order_item:
        if x[1]<0:
            continue        
        quantity.append(int(x[1]))

    amt = []
    # print(menu_item[0][0][4])
    # print(quantity)
    for i in range(len(menu_item)):
        amt.append(quantity[i]*menu_item[i][0][4])
    # print(amt)
      
    total = sum(amt)
      

    db.close()
    return render(request,'AddToCart.html',{'menu':menu_item,'quantity':quantity,'amt':amt,'total':total,'username':username})   

def updatecart(request):
    db,cmd = connection()

    data  = json.loads(request.body)
  
    menuId = data['productId']
    
    action = data['action']
    
    username = data['username']
    
    q1="select uid from user_table where username='{0}'".format(username)
    cmd.execute(q1)
    uid = cmd.fetchone()
    db.commit()
    
    if uid is None:
        uid = " "

    transaction_id = urlsafe_base64_encode(force_bytes(action+str(uid[0])))
    date = datetime.now()
    print(date)
    false= False
    
    find = "select order_id from restro_db.order where uid='{0}'".format(uid[0])
    cmd.execute(find)
    user = cmd.fetchone()
    # print(user)

    db.commit()

    if action == 'add':
    # this is to check if user is already present in order table or not
        if user is None:
        # if not present then insert into order table
            q2= "INSERT INTO restro_db.order (transaction_id,uid,order_date,complete) VALUES ('{0}','{1}','{2}','{3}')".format(transaction_id,uid[0],date,false)
            cmd.execute(q2)
            db.commit()
        # to fetch order_id from order table
            q3 = "select order_id from restro_db.order where uid='{0}'".format(uid[0])
            cmd.execute(q3)
            order_id = cmd.fetchone()
            db.commit()
        # to set itmes in order_item table
            q4 = "insert into restro_db.order_item (order_id,menu_id,quantity) values ('{0}','{1}','{2}')".format(order_id[0],menuId,1)
            cmd.execute(q4)
            db.commit()
        
        else:
        # if present then update order_item table
        # this is to check if item is already present in order_item table or not
     
            print("user data in not none it is already present ")
            # check if item is already present in order_item table or not
            q5 = "select * from restro_db.order_item where order_id='{0}' and menu_id='{1}'".format(user[0],menuId)
            cmd.execute(q5)
            item = cmd.fetchone()
            db.commit()
            print(item)
            if item is None:
            # if not present then insert into order_item table
                q6 = "insert into restro_db.order_item (order_id,menu_id,quantity) values ('{0}','{1}','{2}')".format(user[0],menuId,1)
                cmd.execute(q6)
                db.commit()
            else:
            # if present then update order_item table
                q7 = "update restro_db.order_item set quantity=quantity+1 where order_id='{0}' and menu_id='{1}'".format(user[0],menuId)
                cmd.execute(q7)
                db.commit()

    else:
# this is to check quantity of item in order_item table
        q5 = "select quantity from restro_db.order_item where order_id = '{0}' and menu_id = '{1}'".format(user[0],menuId)
        cmd.execute(q5)
        quantity = cmd.fetchone()
        db.commit()
        print(quantity)
        if quantity[0] == 1:
            q6 = "delete from restro_db.order_item where order_id = '{0}' and menu_id = '{1}'".format(user[0],menuId)
            cmd.execute(q6)
            db.commit()
        else:
            q7 = "update restro_db.order_item set quantity = quantity-1 where order_id = '{0}' and menu_id = '{1}'".format(user[0],menuId)
            cmd.execute(q7)
            db.commit()
        
    db.close()
    return JsonResponse("updated item",safe=False)


def CheckOut(request, username):
    db,cmd = connection()
    q="select uid from user_table where username='{0}'".format(username)
    cmd.execute(q)
    uid = cmd.fetchall()
    db.commit()
    
    q2="select order_id from restro_db.order where uid='{0}'".format(uid[0][0])
    cmd.execute(q2)
    order_id = cmd.fetchall()
    db.commit()

    q3="select menu_id, quantity from restro_db.order_item where order_id={0}".format(order_id[0][0])
    cmd.execute(q3)
    order_item = cmd.fetchall()
    db.commit()

    menu_item = []
    for i in order_item:
        q4="select * from restro_db.menu where menu_id={0}".format(i[0])
        cmd.execute(q4)
        menu_item.append(cmd.fetchall())
        db.commit()
    
    quantity = []
    for x in order_item:
        if x[1]<0:
            continue        
        quantity.append(int(x[1]))

    amt = []
    # print(menu_item[0][0][4])
    # print(quantity)
    for i in range(len(menu_item)):
        amt.append(quantity[i]*menu_item[i][0][4])
    # print(amt)
      
    total = sum(amt)
      

    db.close()
    return render(request,'CheckOut.html',{'total':total,'quantity':quantity,'amt':amt,'menu':menu_item})



def shipping(request):
    city = request.POST.get('city')
    state = request.POST.get('state')
    address = request.POST.get('address')
    zipcode = request.POST.get('zipcode')
    name = request.POST.get('name')
    email = request.POST.get('email')
    username = request.COOKIES.get('CookiesUsername')  
    password = request.COOKIES.get('CookiesPassword')
    print(city,state,address,zipcode,name,email)
    db,cmd = connection()
    

    q="select uid from user_table where username='{0}'".format(username)
    cmd.execute(q)
    uid = cmd.fetchall()
    print(uid[0][0])
    db.commit()
    q1 = "select order_id from restro_db.order where uid='{0}'".format(uid[0][0])
    cmd.execute(q1)
    order_id = cmd.fetchall()
    print(order_id[0][0])
    print(type(order_id[0][0]))
    db.commit()

    
    q3="select menu_id, quantity from restro_db.order_item where order_id={0}".format(order_id[0][0])
    cmd.execute(q3)
    order_item = cmd.fetchall()
    db.commit()

    menu_item = []
    for i in order_item:
        q4="select * from restro_db.menu where menu_id={0}".format(i[0])
        cmd.execute(q4)
        menu_item.append(cmd.fetchall())
        db.commit()
    
    quantity = []
    for x in order_item:
        if x[1]<0:
            continue        
        quantity.append(int(x[1]))

    amt = []
    # print(menu_item[0][0][4])
    # print(quantity)
    for i in range(len(menu_item)):
        amt.append(quantity[i]*menu_item[i][0][4])
    # print(amt)
    total = sum(amt)
    q3 = "insert into restro_db.shiping_address (uid,order_id,address,city,state,zipcode,date_added) values ('{0}',{1},'{2}','{3}','{4}','{5}','{6}')".format(uid[0][0],order_id[0][0],address,city,state,zipcode,datetime.now())
    cmd.execute(q3)
    db.commit()
    db.close()
   
    return render(request,'shipping.html',{'city':city,'state':state,'address':address,'zipcode':zipcode,'name':name,'email':email,'total':total,'quantity':quantity,'amt':amt,'menu':menu_item})

    

def recipe(request):
    return render(request,'recipe.html')


def searchResult(request):
    result = request.POST.get('search')

    return render(request,'searchResult.html',{"result":result})


