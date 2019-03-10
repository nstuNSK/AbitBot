# -*- coding: utf-8 -*-


import json

def get_button(label, color,payload=""):
    return{
        "action":
        {
            "type":"text",
            "payload":json.dumps(payload),
            "label":label
        },
        "color": color
    }
def convertToString(keyboard):
    return json.dumps(keyboard, ensure_ascii = False)

def get_keyboards():

    keyboard_start = {
        "one_time": True,
        "buttons":[
            [get_button(label="Начать",color="primary", payload="admin")]
        ]
    }
    keyboard_start = convertToString(keyboard_start)


    keyboard_main_menu_off = {
        "one_time": True,
        "buttons":[
            [get_button(label="Подписаться на новости",color="default",payload="subscribe")],
            [get_button(label="Подбор направления",color="default",payload="direction_selection")],
            [get_button(label="Конкурсные списки",color="default",payload="lists")]
        ]
    }
    keyboard_main_menu_off = convertToString(keyboard_main_menu_off)

    keyboard_main_menu_on = {
        "one_time": True,
        "buttons":[
            [get_button(label="Отписаться от новостей",color="default",payload="subscribe")],
            [get_button(label="Подбор направления",color="default",payload="direction_selection")],
            [get_button(label="Конкурсные списки",color="default",payload="lists")]
        ]
    }
    keyboard_main_menu_on = convertToString(keyboard_main_menu_on)


    keyboard_subscribe={
        "one_time": True,
        "buttons":[
            [get_button(label="Для школьника",color="default", payload="schoolchild")],
            [get_button(label="Для поступающего",color="default",payload="enrollee")]
        ]
    }
    keyboard_subscribe = convertToString(keyboard_subscribe)


    keyboard_direction_selection = {
        "one_time": True,
        "buttons":[
            [get_button(label="По предметам",color="default",payload="name_dir")],
            [get_button(label="По сфере",color="default",payload="sphere")],
            [get_button(label="Главное меню",color="primary",payload="main_menu")]
        ]
    }
    keyboard_direction_selection = convertToString(keyboard_direction_selection)

    keyboard_list = {
        "one_time": True,
        "buttons":[
            [get_button(label="Ввести код из ЛК НГТУ",color="default",payload="lk_code")],
            [get_button(label="Частота уведомлений",color="default",payload="frequency")],
            [get_button(label="Главное меню",color="primary",payload="main_menu")]
        ]
    }
    keyboard_list = convertToString(keyboard_list)


    keyboard_sphere = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Машиностроение",color="default",payload="Машиностроение"),
                get_button(label="Безопасность",color="default",payload="Безопасность")
            ],
            [
                get_button(label="Энергетика",color="default",payload="Энергетика"),
                get_button(label="IT",color="default",payload="IT-технологии"),
                get_button(label="Электроника",color="default",payload="Электроника")
            ],
            [
                get_button(label="Авиация",color="default",payload="Авиация"),
                get_button(label="Общество",color="default",payload="Общество"),
                get_button(label="Экономика",color="default",payload="Экономика")
            ],
            [
                get_button(label="Химия",color="default",payload="Химия"),
                get_button(label="Языки",color="default",payload="Языки"),
                get_button(label="Физика",color="default",payload="Физика")
            ],
            [
                get_button(label="Главное меню",color="primary",payload="main_menu"),
                get_button(label = "Найти", color = "primary", payload = "search_by_sphere")
            ]
        ]
    }
    keyboard_sphere = convertToString(keyboard_sphere)


    keyboard_subjects = {
        "one_time": True,
        "buttons":[
            [
                get_button(label="Математика",color="default",payload="Математика"),
                get_button(label="Биология",color="default",payload="Биология"),
                get_button(label="География",color="default",payload="География"),
                get_button(label="Иностранный язык",color="default",payload="Иностранный язык")
            ],
            [
                get_button(label="Информатика",color="default",payload="Информатика"),
                get_button(label="История",color="default",payload="История"),
                get_button(label="Литература",color="default",payload="Литература")
            ],
            [
                get_button(label="Обществознание",color="default",payload="Обществознание"),
                get_button(label="Физика",color="default",payload="Физика"),
                get_button(label="Химия",color="default",payload="Химия")
            ],
            [
                get_button(label="Главное меню",color="primary",payload="main_menu"),
                get_button(label = "Найти", color = "primary", payload = "search_by_subjects")
            ]
        ]
    }
    keyboard_subjects = convertToString(keyboard_subjects)


    keyboard_frequency = {
        "one_time": True,
        "buttons":[
            [get_button(label="Один раз в день",color="default",payload="one_per_day")],
            [get_button(label="Два раза в день",color="default",payload="two_per_day")],
        ]
    }
    keyboard_frequency = convertToString(keyboard_frequency)
    return{
        'start': keyboard_start,
        'main_menu_on': keyboard_main_menu_on,
        'main_menu_off':keyboard_main_menu_off,
        'subscribe': keyboard_subscribe,
        'direction_selection': keyboard_direction_selection,
        'list': keyboard_list,
        'sphere': keyboard_sphere,
        'subjects': keyboard_subjects,
        'frequency':keyboard_frequency
    }