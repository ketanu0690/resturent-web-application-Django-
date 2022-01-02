# from django.shortcuts import render  
# from django.http import HttpResponse  
# from .pool import connection

# def setcookiedata(request,uid):
#     db,cmd = connection()
#     q="select * from user_table where username='{0}'".format(uid)
#     cmd.execute(q)
#     user=cmd.fetchone()
#     db.commit()
#     # cookie_value = user
#     # response = HttpResponse('blah')
#     # response.set_cookie('cookie_name', cookie_value , max_age=60*60*24*365)
#     response = HttpResponse("Cookie Set")  
#     response.set_cookie('java-tutorial', 'javatpoint.com') 
#     return response

# def get_cookie_data(request):
#   cookie_value = request.COOKIES['cookie_name']
#   return HttpResponse(cookie_value)



