try:
    from bot.bot import SERVICE_KEY, auth
    from administrator.models import *
    from AbitBot.settings import MEDIA_ROOT
except:
    pass

import requests
import csv
import json
import vk_api


def upgrade_csv():
    import numpy as np
    try:
        # this piece of code must be include instead test data
        data = Account.objects.all()
        users = []
        for user in data:
            users.append(str(user.id))
        users = ",".join(users)
        
        # res = {"cities": [], "schools": [], "sex": {"male": 0, "female": 0}, "bdate": []}
        vk = auth()

        # test data
        # users = ["227017896", "176468928",
        #         "maslennikova7", "serdeshkoed",
        #         "makcgan", "mazzepa4x4",
        #         "53489652", "stas_agafonov",
        #         "tohuntskristina", "317150640",
        #         "vladislavagerasimova", "", 
        #         "durnev_in", "sergeevski", 
        #         "mmmoouse", "urrow_art", 
        #         "niceadmen", "lisa.antokhina", 
        #         "westfronz", "sweetgirl75", 
        #         "346387551", "5939889", 
        #         "kvshvets", "k.whale", 
        #         "127749491", "16871600", 
        #         "f0rz1k", "soullessprincess", 
        #         "165243327", "514368777", 
        #         "165194054", "nadezhda_borisova", 
        #         "kovalskykovalsky", "384160085", 
        #         "victoriaorl", "romannsk1984", 
        #         "sergey_chuprov", "nikolya947", 
        #         "144667416", "giros_baydi", 
        #         "nadin_aladin", "95151469", 
        #         "kyudina2014", "mikelpopov", 
        #         "aigrm", "ktpalucard", 
        #         "21064803", "iost_aleksey",
        #         "377779744", "korepanlox",
        #         "drrakunovaa", "daria_timofeeva21",
        #         "148145405", "id_belimov_2002",
        #         "162847294", "231765761",
        #         "217358084", "chilyaa",
        #         "ekaterinaaa_17", "111171491",
        #         "86386235", "nikitamalinkin",
        #         "lamii777", "stasia974",
        #         "nadia_milka", "mr.pickless",
        #         "lskazhutina", "valeria.kulikova",
        #         "numberr24", "krooglick411",
        #         "alena_barrrskix"]
        # users = list(set(users)) #this code is temp
        # users = ",".join(users)
        info = vk.method("users.get", {"user_ids": users, "fields": "sex,city,bdate,education,schools"})
        for i in info:
            if "deactivated" in i:
                del(i)
            else:
                if "city" in i:
                    i["city"] = i["city"]["title"]
                if "schools" in i:
                    if len(i["schools"]) == 0:
                        i["schools"] = None
                    else:
                        l = len(i["schools"])
                        i["schools"] = i["schools"][l-1]["name"]

            
        # keys = []
        # for i in info:
        #     keys.extend(i.keys())
        # keys = list(set(keys))
        keys = ["id", "first_name", "last_name", "city",
                "sex", "bdate", "university",
                "university_name", "faculty", "faculty_name", "education_form", "education_status",
                "graduation", "schools",  "is_closed", "can_access_closed", "deactivated"]
        with open(MEDIA_ROOT+"/file.csv", 'w') as myfile:
            wr = csv.DictWriter(myfile, fieldnames = keys)
            wr.writeheader()
            for i in info:
                wr.writerow(i)
        return True
    except:
        raise
        return False


def get_stat_from_csv():
    import pandas as pd
    import datetime as dt

    data = pd.read_csv(MEDIA_ROOT+"/file.csv",
                       sep=',', encoding='utf-8')
    sex = data["sex"].value_counts()
    cities = data["city"].value_counts()
    schools = data["schools"].value_counts()
    ages = {"b16": 0, "f16to22": 0, "a22": 0, "none": 0}
    for i in data["bdate"]:
        if len(str(i)) > 5:
            index = i.rfind(".")
            year = i[index+1:]
            age = dt.datetime.now().year-int(year)
            if age < 16:
                ages["b16"] = ages["b16"]+1
            elif age > 22:
                ages["a22"] = ages["a22"]+1
            else:
                ages["f16to22"] = ages["f16to22"]+1
        else:
            ages["none"] = ages["none"]+1

    return {"sex": sex.to_dict(), "cities": cities.to_dict(), "schools": schools.to_dict(), "ages": ages, "count": len(data)}
            

        
            

# if __name__ == "__main__":
#     # upgrade_csv()
#     get_stat_from_csv()