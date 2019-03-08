from .models import *

import requests
import json

#?json_indent=1&decode_unicode_escape=1
def configure():
    url = "https://api.ciu.nstu.ru/v1.0/test/for_bot"


    r = requests.get(url)
    res = json.loads(r.content.decode("utf-8"))

    for direction in res:
        dir = Direction.objects.get_or_create( name = direction["DIRECTION"], 
                                        faculty = direction["FACULT"],
                                        keys_plus = direction["KEYS_PLUS"],
                                        ball_k = direction["BALL_K"],
                                        ball_b = direction["BALL_B"],
                                        url = direction["URL"],
                                        description = direction["DESCR"],
                                        profile_name = direction["PROFILE_NAME"],
                                        id = direction["ID"])
        print(dir[0])
        spheres = direction["data"]
        if spheres[0]["SPHERE"] != None:
            for sphere in spheres:
                s = Sphere.objects.get_or_create(name = sphere["SPHERE"])
                s[0].direction.add(dir[0])
        subjects = [direction["DISC1"], direction["DISC2"], direction["DISC3"]]
        for subject in subjects:
            s = Subject.objects.get_or_create(name = subject)
            s[0].direction.add(dir[0])

def create_msgs():
    msgs = [
        ["SEARCH_DIRECTION_START", "Вот что я нашел🙃"],
        ["SEARCH_DIRECTION_START", "Понеслась!"],
        ["SEARCH_DIRECTION_START", "Уже нашел!"],
        ["SEARCH_DIRECTION_START", "Так-так-так, что тут у нас?"],
        ["SEARCH_DIRECTION_END", "Искал как в последний раз😂"],
        ["SEARCH_DIRECTION_END", "Заставил же ты меня потрудиться!😁"],
        ["SEARCH_DIRECTION_END", "Фух... устал..."],
        ["SEARCH_DIRECTION_ERROR", "Но... ты... же... ничего не добавил..."],
        ["START", "Привет, я бот Йети✋🏻\n\nИ я твой персональный помощник в мире НГТУ😎😎😎\nЯ могу помочь тебе с поступлением или просто рассказать о НГТУ и обо всем, что с ним связано😎"],
        ["HELP_MSG", "Итак, чем я могу тебе помочь?"],
        ["ADMIN", "Опять по новой? Ну, ладно..."],
        ["MAIN_MENU", "Сделал!"],
        ["SUBSCRIBE", "Теперь я буду отправлять тебе новости! Люблю это😍"],
        ["UNSUBSCRIBE", "Не хочешь, как хочешь...\тНо, если передумаешь, я всегда готов💪🏻"],
        ["DIRECTION_SELECTION", "А как подобрать напрваление?"],
        ["SPHERE", "Подскажи сферы, а то тут много😊"],
        ["ADD_MSG", "Добавил! Это было легко😉"],
        ["ADD_MSG", "Проще простого! Добавил!"],
        ["ADD_MSG", "Изи добавил!"],
        ["ADD_MSG", "Плюс один😉"],
        ["NAME_DIR", "По каким предметам будем искать?\nРусский язык нужен для всех направлений, поэтому я его уже добавил😊"],
        ["FEAR_MSG", "Аааа! Не пугай!"],
        ["ERROR", "Я тебя не понимаю😔\nИспользуй, пожалуйста, клавиатуру🙏🏻"],
        ["NEWS_START", "Вот, принес тебе последние новости😊"],
        ["NEWS_END", "Пока все😊"]
    ]
    for item in msgs:
        Msg.objects.get_or_create(pay = item[0], msg = item[1])


