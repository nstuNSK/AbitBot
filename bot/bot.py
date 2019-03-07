import vk_api
import random
import time
import json
import sys
import requests
from . import keyboards
#import api_nstu_news as api
from administrator.models import *

def auth():
    vk = vk_api.VkApi(token='d00a1318d5f9182d89e56612d1df321e3413ca74c2b6cb6a6fe443cb0782adbcbf089960703bfda62658b')
    vk._auth_token()
    return vk

def from_pay_to_msg(pay):
    msgs = Msg.objects.filter(pay = pay).values()
    #!!!!
    return msgs

def search_direction(user, type):
    dir = []
    if type == "SPHERE":
        spheres = user.spheres.all()
        for sphere in spheres:
            dir.append(sphere.directions.all)
    elif type == "SUBJECTS":
        subjects = user.subjects.all()
        for subject in subjects:
            dir.append(subject.directions.all)
    if len(dir)!=0:
        vk.method("messages.send", {"user_id": user.id,"message":random.choice(from_pay_to_msg("SEARCH_DIRECTION_START"))[0]})
        response = ""
        for item in dir:
            if item.profile_name == None:
                response = response + "Направление: " + '"' + item.name + '"' + " на факультете " + item.faculty + "\n" +"Ссылка на направление: " + item.url+"\n\n"
            else:
                response = response + "Направление: " + '"' + item.name + ' (' + item.profile_name + ')' + '"' + " на факультете " + item.faculty+ "\n" +"Ссылка на направление: " + item.url+"\n\n"
            if(len(response)>3500):
                vk.method("messages.send", {"user_id": user.id,"message": response})
                response = ""
        if(response!=""):
            vk.method("messages.send", {"user_id": user.id,"message": response})
        vk.method("messages.send", {"user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_END"))[0], 'keyboard': get_main_keyboard(user = user)})
    else:
        if type == "SPHERE":
            vk.method("messages.send", {"user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR"))[0], 'keyboard': key['sphere']})
        elif type == "SUBJECTS":
            vk.method("messages.send", {"user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR"))[0], 'keyboard': key['subjects']})

def add_sub(user, sub):
    subject = Subject.objects.get(name = sub)
    subject.account.add(user)

def add_sphere(user, pay):
    sphere = Sphere.objects.get(name = pay)
    sphere.account.add(user)

def get_main_keyboard(user):
    if user.subscribe == True:
        return key['main_menu_on']
    else:
        return key['main_menu_off']

def data_processing(id, pay, msg):
    user = Account.objects.get_or_create(id = id)[0]
    if pay=={"command":"start"} or pay == "admin":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("START"))[0]})
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("HELP_MSG"))[0], "keyboard": get_main_keyboard(user = user)})
    
    elif msg=="admin":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADMIN"))[0], "keyboard":key['start']})
    
    elif pay == "main_menu":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("MAIN_MENU"))[0], "keyboard":get_main_keyboard(user = user)})

    elif pay=="subscribe":
        if user.subscribe == False:
            user.update(subscribe = True)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("SUBSCRIBE"))[0], 'keyboard': get_main_keyboard(user = user)})
        else:
            user.update(subscribe = False)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("UNSUBSCRIBE"))[0], 'keyboard': get_main_keyboard(user = user)})
    
    elif pay=="direction_selection":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("DIRECTION_SELECTION"))[0], "keyboard":key['direction_selection']})
    
    elif pay=="sphere":
        user.update(sphere = None)
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("SPHERE"))[0], "keyboard":key['sphere']})
    
    elif pay=="Машиностроение" or pay=="Безопасность" or pay=="Энергетика" or pay=="IT-технологии" or pay=="Электроника" or pay=="Авиация" or pay=="Общество" or pay=="Экономика" or pay=="Химия" or pay=="Языки" or pay=="Физика":
        spheres = user.spheres.all()
        if len(spheres) != 0:
            if len(spheres) < 3:
                add_sphere(user = user, pay = pay)
                vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['sphere']})
                if len(spheres)+1>=3:
                    search_direction(user = user, type = "SPHERE")
        else:
            add_sphere(user = user, pay = pay)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['sphere']})
        
   
    elif pay=="name_dir":
        user.update(subjects = None)
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("NAME_DIR"))[0], "keyboard":key['subjects']})

    elif pay == "math" or pay == "biology" or pay == "geography" or pay == "foreign_language" or pay == "informatics" or pay == "history" or pay == "literature" or pay == "social_science" or pay == "physics" or pay == "chemistry":
        sub = user.subjects.all()
        if len(sub) !=0:
            if len(sub)<2:
                add_sub(user = user, sub = pay)
                vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['subjects']})
                if(len(sub)+1>=2):
                    search_direction(id = id, type = "SUBJECTS")#!!!!
        else:
            add_sub(user = user, sub = pay)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['subjects']})
    
    elif pay == "search_by_sphere":
        search_direction(user = user, type = "SPHERE")
    elif pay == "search_by_subjects":
        search_direction(user = user, type = "SUBJECTS")
    elif pay == "lists":
        vk.method("messages.send", {"user_id": id, "message": "Выберите функцию:", "keyboard": key['list']})
    
    elif pay == "lk_code":
        vk.method("messages.send", {"user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": get_main_keyboard(user = user)})
    
    elif pay == "frequency":
        vk.method("messages.send", {"user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": get_main_keyboard(user = user)})
    
    elif msg == "Бу!":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("FEAR_MSG"))[0], "keyboard": get_main_keyboard(user = user)})
    else:
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ERROR"))[0], "keyboard": get_main_keyboard(user = user)})

key = keyboards.get_keyboards() 
vk = auth()