# -*- coding: utf-8 -*-
import vk_api
import random
import time
import json
import sys
import requests
from datetime import datetime
from django.db.models import F
from . import keyboards
#import api_nstu_news as api
from administrator.models import *
from django.core.paginator import Paginator

SERVICE_KEY = "c1a71290c1a71290c1a71290b7c1cfa9fecc1a7c1a712909dcf1906a5e4cdbd9fbe3703"
FREQUENCY_FEEDBACK = 0.9

def auth():
    vk = vk_api.VkApi(token='f77e482fc0da16105d5dc35579dc14009893764743111e79864369756790fe6f0f688f6a01bb41ac2039c')
    vk._auth_token()
    return vk

def from_pay_to_msg(pay):
    msgs = Msg.objects.filter(pay = pay)
    res = []
    for msg in msgs:
        res.append(msg.msg)
    return res

def get_directions_from_page(dir, prev_page):
    p = Paginator(dir, 3)
    if prev_page != 0:
        page = p.page(prev_page)
        if page.has_next():
            page = p.page(prev_page+1)
            return (page.object_list, page.has_next())
        else:
            return ([], False)
    else:
        try:
            page = p.page(1)
            return (page.object_list, page.has_next())
        except:
            return ([False],False)

def get_temp_keyboard(type, page, has_next):
    key = {
            "one_time": True,
            "buttons":[
                [keyboards.get_button(label="Главное меню",color="primary",payload="main_menu")],
            ]
        }
    if has_next:
        if type == "SPHERE":
            key["buttons"].insert(0, [keyboards.get_button(label="Еще",color="primary",payload="{'pay':'search_by_sphere', 'page':"+str(page)+"}")])
        else:
            key["buttons"].insert(0, [keyboards.get_button(label="Еще",color="primary",payload="{'pay':'search_by_subjects', 'page':"+str(page)+"}")])
    
    return keyboards.convertToString(key)
    

def search_direction(user, type, extra = 0):
    dir = []
    if type == "SPHERE":
        mas = user.spheres.all()
        for item in mas:
            directions = item.direction.all()
            for direction in directions:
                if direction not in dir:
                    dir.append(direction)
    elif type == "SUBJECTS":
        mas = user.subjects.all()
        directions = mas[0].direction.all()
        for direction in directions:
            flag = True
            for item in mas:
                if item not in direction.subjects.all():
                    flag = False
            if flag:
                dir.append(direction)
    
    dir.sort(key = lambda x: x.RN, reverse = False)
    r = get_directions_from_page(dir, extra)
    dir = r[0]
    has_next = r[1]
    temp_keyboard = get_temp_keyboard(type, extra, has_next)


    if len(dir)!=0:
        #test
        if dir[0] == False:
            user.random_id = user.random_id + 1
            user.save()
            if type == "SPHERE":
                if len(user.spheres.all()) == 0:
                    vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR")), 'keyboard': key['sphere']})
                else:
                    vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_NOT_FOUND")), 'keyboard': get_main_keyboard(user = user)})
            elif type == "SUBJECTS":
                if len(user.subjects.all()) == 0:
                    vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR")), 'keyboard': key['subjects']})
                else:
                    vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_NOT_FOUND")), 'keyboard': get_main_keyboard(user = user)})
        else:
            if extra == 0:
                user.random_id = user.random_id + 1
                user.save()
                vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message":random.choice(from_pay_to_msg("SEARCH_DIRECTION_START"))})
            response = ""
            for item in dir:
                try:
                    if item.profile_name == None:
                        response = response + "Направление: " + '"' + item.name + '"' + " на факультете " + item.faculty + "\n" +"Ссылка на направление: " + item.url+"\n\n"
                    else:
                        response = response + "Направление: " + '"' + item.name + ' (' + item.profile_name + ')' + '"' + " на факультете " + item.faculty+ "\n" +"Ссылка на направление: " + item.url+"\n\n"
                    if len(response)>3500:
                        user.random_id = user.random_id + 1
                        user.save()
                        vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": response, "keyboard": temp_keyboard})
                        response = ""
                except Exception as e:
                    user.random_id = user.random_id + 1
                    user.save()
                    vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": e})
            # if response!="":
            #     user.random_id = user.random_id + 1
            #     user.save()
            #     vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": response})
            # user.random_id = user.random_id + 1
            # user.save()
            # vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_END")), 'keyboard': get_main_keyboard(user = user)})
    else:
        user.random_id = user.random_id + 1
        user.save()
        vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_END")), 'keyboard': get_main_keyboard(user = user)})

        # user.random_id = user.random_id + 1
        # user.save()
        # if type == "SPHERE":
        #     if len(user.spheres.all()) == 0:
        #         vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR")), 'keyboard': key['sphere']})
        #     else:
        #         vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_NOT_FOUND")), 'keyboard': get_main_keyboard(user = user)})
        # elif type == "SUBJECTS":
        #     if len(user.subjects.all()) == 0:
        #         vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR")), 'keyboard': key['subjects']})
        #     else:
        #         vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_NOT_FOUND")), 'keyboard': get_main_keyboard(user = user)})

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

def get_questions(pay,user):
    #try:
        flag = True
        id = int(pay[1:])
        question = Question.objects.get(id = id)
        test = question.test.all()[0]
        results = user.tests.filter(test = test)
        if len(results)==0:
            result = ResultOfTest.objects.create(test = test)
            result.account.add(user)
        else:
            result = results[0]
            result.allAnswer = 0
            result.rightAnswer = 0
            result.save()
        vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id, "message": str(question.question), "keyboard": keyboards.get_question_keyboard(question = question)})
        #return True
    #except:
    #    return False

def get_result(pay,user):
    id = int(pay[1:])
    answer = Answer.objects.get(id = id)
    question = answer.question.all()[0]
    test = question.test.all()[0]
    result = user.tests.get(test = test)
    result.allAnswer = result.allAnswer + 1
    vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id, "message": str(answer.reaction)})
    user.random_id = user.random_id + 1
    user.save()
    if (answer.is_true):
        result.rightAnswer = result.rightAnswer + 1
    result.save()
    try:
        if len(test.questions.filter(number = question.number+1)) != 0:
            question = Question.objects.get(id = question.id+1)
            vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id, "message": str(question.question), "keyboard": keyboards.get_question_keyboard(question = question)})
        else:
            string = "Твой результат: " + str(result.rightAnswer) + " правильных ответов из " + str(result.allAnswer)
            vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id, "message": string, "keyboard": get_main_keyboard(user = user)})
    except:
        string = "Твой результат: " + str(result.rightAnswer) + " правильных ответов из " + str(result.allAnswer)
        vk.method("messages.send", {"random_id": user.random_id, "user_id": user.id, "message": string, "keyboard": get_main_keyboard(user = user)})


def data_processing(id, pay, msg):
    user = Account.objects.get_or_create(id = id)[0]
    if pay=='"command":"start"' or pay == "admin" or "привет" in msg.lower():
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("START"))})
        user.random_id = user.random_id + 1
        user.save()
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("HELP_MSG")), "keyboard": get_main_keyboard(user = user)})
    if pay == "engineering_works":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": "Извините, ведутся технические работы. Напишите мне позже:)", "keyboard":get_main_keyboard(user = user)})
    elif msg=="admin":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("ADMIN")), "keyboard":key['start']})

    elif pay == "main_menu":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("MAIN_MENU")), "keyboard":get_main_keyboard(user = user)})
        # if user.feedback != "never" and user.feedback != "true":
        #     if user.feedback == "false":
        #         num = random.random()
        #         if num >= FREQUENCY_FEEDBACK:
        #             vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("MAIN_MENU")), "keyboard":key['feedback']})
        #             user.feedback = datetime.now().date().strftime("%d.%m.%Y")
        #             user.save()
        #     else:
        #         time = user.feedback
        #         date = datetime.strptime(time, "%d.%m.%Y").date()
        #         days = (datetime.now().date() - date).days
        #         if days > 6:
        #             vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("MAIN_MENU")), "keyboard": key['feedback']})
        #             user.feedback = datetime.now().date().strftime("%d.%m.%Y")
        #             user.save()
        # else:
        #     vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("MAIN_MENU")), "keyboard":get_main_keyboard(user = user)})

    elif pay=="subscribe":
        if user.subscribe == False:
            user.subscribe = True
            user.save()
            vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("SUBSCRIBE")), 'keyboard': get_main_keyboard(user = user)})
        else:
            user.subscribe = False
            user.save()
            vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("UNSUBSCRIBE")), 'keyboard': get_main_keyboard(user = user)})
    elif pay=="direction_selection":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("DIRECTION_SELECTION")), "keyboard":key['direction_selection']})

    elif pay=="sphere":
        spheres = user.spheres.all()
        for sphere in spheres:
            sphere.account.remove(user)
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("SPHERE")), "keyboard":key['sphere']})

    elif pay=="Машиностроение" or pay=="Безопасность" or pay=="Энергетика" or pay=="IT-технологии" or pay=="Электроника" or pay=="Авиация" or pay=="Общество" or pay=="Экономика" or pay=="Химия" or pay=="Языки" or pay=="Физика":
        spheres = user.spheres.all()
        length = len(spheres)
        if  length!= 0:
            if length < 2:
                add_sphere(user = user, pay = pay)
                length = length + 1
                if length>=2:
                    search_direction(user = user, type = "SPHERE")
                else:
                    vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG")), "keyboard":key['sphere']})
        else:
            add_sphere(user = user, pay = pay)
            vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG")), "keyboard":key['sphere']})

    elif pay=="name_dir":
        subjects = user.subjects.all()
        for sub in subjects:
            sub.account.remove(user)
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("NAME_DIR")), "keyboard":key['subjects']})

    elif pay == "математика" or pay == "биология" or pay == "география" or pay == "иностранный язык" or pay == "информатика" or pay == "история" or pay == "литература" or pay == "обществознание" or pay == "физика" or pay == "химия":
        l = list(pay)
        l[0] = l[0].upper()
        pay = "".join(l)
        sub = user.subjects.all()
        length = len(sub)
        if length !=0:
            if length<2:
                add_sub(user = user, sub = pay)
                length = length + 1
                if length>=2:
                    search_direction(user = user, type = "SUBJECTS")
                else:
                     vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG")), "keyboard":key['subjects']})
        else:
            add_sub(user = user, sub = pay)
            vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG")), "keyboard":key['subjects']})

    elif pay == "search_by_sphere":
        search_direction(user = user, type = "SPHERE")

    elif pay == "search_by_subjects":
        search_direction(user = user, type = "SUBJECTS")

    elif pay == "lists":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": "Выберите функцию:", "keyboard": key['list']})

    elif pay == "lk_code":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": get_main_keyboard(user = user)})

    elif pay == "frequency":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": get_main_keyboard(user = user)})

    elif pay=="tests":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": "Выбери тест", "keyboard": keyboards.get_tests_keyboard(l = 1)})

    elif pay[0]=="Q":
        get_questions(pay = pay, user = user)

    elif pay[0]=="A":
        get_result(pay = pay, user = user)

    elif msg == "Бу!":
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("FEAR_MSG")), "keyboard": get_main_keyboard(user = user)})
    else:
        vk.method("messages.send", {"random_id": user.random_id, "user_id": id, "message": random.choice(from_pay_to_msg("ERROR")), "keyboard": get_main_keyboard(user = user)})
    user.random_id = user.random_id + 1
    user.save()

key = keyboards.get_keyboards()
vk = auth()