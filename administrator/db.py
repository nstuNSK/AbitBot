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




