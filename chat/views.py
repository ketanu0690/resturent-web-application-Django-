from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
# from chat.models import Room, Message
from restro.pool import connection
from django.http import HttpResponse, JsonResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
import numpy as np
import nltk
import string
import random
# Create your views here.
def home(request):
    

    return render(request, 'chatroom/home.html')


def chatbot(request):
    msg = request.POST['msg']
    flag = request.POST['flag']
    flag=flag
    user_response = msg
    user_response=user_response.lower()
    print(msg)
    f=open('chatbot.txt','r', errors = 'ignore')
    raw_doc=f.read()
    raw_doc=raw_doc.lower() #Converts text to lowercase
    # nltk.download('punkt') #Using the Punkt tokenizer
    # nltk.download('wordnet') #Using the WordNet dictionary
    sent_tokens = nltk.sent_tokenize(raw_doc) #Converts doc to list of sentences
    word_tokens = nltk.word_tokenize(raw_doc) #Converts doc to list of words
    lemmer = nltk.stem.WordNetLemmatizer()

    def LemTokens (tokens):
        return [lemmer.lemmatize(token) for token in tokens]
    remove_punct_dict = dict ((ord(punct), None) for punct in string.punctuation)
    def LemNormalize(text): 
        return LemTokens (nltk. word_tokenize(text.lower().translate(remove_punct_dict)))

    GREET_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey")
    GREET_RESPONSES = ["hi", "hey", "hi there", "hello", "I am glad! You are talking to me"]


    def greet(sentence):
        for word in sentence.split():
            if word.lower() in GREET_INPUTS:
                return random.choice(GREET_RESPONSES)    

    def response(user_response):
        robo1_response=''
        TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
        tfidf = TfidfVec.fit_transform(sent_tokens)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]

        if(req_tfidf==0):
            robo1_response=robo1_response+"I am sorry! I don't understand you ,may i connect you to our customer care service"
            return robo1_response

        else:
            robo1_response = robo1_response+sent_tokens [idx]
            return robo1_response

    if(user_response!='bye'):
        if(user_response=='thanks' or user_response=='thank you' ):
            flag="False"
            return JsonResponse({'msg':'You are welcome..'})
            # return HttpResponse("You are welcome..")
        elif (user_response== 'find rasturent near me'):
            return JsonResponse({'msg':'find rasturent near me'})
         
           
        else:
                if(greet (user_response)!=None):
                    # send userresponse to js variable
                    msg = greet(user_response)
                    return JsonResponse({"msg":msg})
                
                else:
                    sent_tokens.append (user_response)
                    word_tokens = word_tokens+nltk.word_tokenize(user_response)
                    final_words=list(set(word_tokens))
                    sent_tokens.remove(user_response)
                    msg = response(user_response)
                    return JsonResponse({"msg":msg})
                    
                    
    else:
        flag="False"
        return JsonResponse({'msg':'Bye! take care..'})

def room(request, room):
    pass
    # username = request.GET.get('username')
    # # room_details = Room.objects.get(name=room)
    # return render(request, 'room.html', {
    #     'username': username,
    #     'room': room,
    #     # 'room_details': room_details
    # })

def checkview(request):
    pass
    # room = request.POST['room_name']
    # username = request.POST['username']

    # db,cmd = connection()

    # if Room.objects.filter(name=room).exists():
    # return redirect('/'+room+'/?username='+username)
    # else:
        # new_room = Room.objects.create(name=room)
        # new_room.save()
    # return redirect('/'+room+'/?username='+username)

def send(request):
    pass
    # message = request.POST['message']
    # username = request.POST['username']
    # room_id = request.POST['room_id']

    # new_message = Message.objects.create(value=message, user=username, room=room_id)
    # new_message.save()
    # return HttpResponse('Message sent successfully')

def getMessages(request, room):
    pass
    # room_details = Room.objects.get(name=room)

    # messages = Message.objects.filter(room=room_details.id)
    # return JsonResponse({"messages":list(messages.values())})