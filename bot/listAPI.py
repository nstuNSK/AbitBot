import requests
import datetime
# from AbitBot import settings

API_KEY = "s13dfget456DADHGWEv34g435f"

# 1. список снапшотов изменений
# URL: /get_snaps или /get_snaps?start_time=:date
# Метод: GET
# Параметры: необязательный date - строка формата "dd.mm.yyyy hh24:mi:ss"
# , задающая, дату, начиная с которой возвращается список
# например: date="16.03.2018 17:00:00"

ROOT_URL = "http://api.ciu.nstu.ru/v1.0/api/abit_bot"
def get_snaps(start_time = 0):
    if isinstance(start_time, int) and start_time == 0:
        res = requests.get(ROOT_URL+"/get_snaps", headers = {"Http-Api-Key": settings.API_KEY})
    else:
        print("here")
        time = start_time.strftime('%d.%m.%Y %H:%M:%S')
        print(time)
        res = requests.get(ROOT_URL+'/get_snaps?start_time='+'"'+time+'"', headers = {"Http-Api-Key": settings.API_KEY})
    if res.status_code == 200:
        return res.json()
    else:
        return False

# 2. Список абитуриентов
# URL: /get_reitings или /get_reitings?start_snap=:snap_id
# Метод: GET
# Параметры: необязательный snap_id - целое число, идентификатор снимка,
# начиная с которого возвращаются изменения
#            например: snap_id=10

def get_reitings(start_snap = -1):
    if start_snap == -1:
        res = requests.get(ROOT_URL+"/get_reitings", headers = {"Http-Api-Key": settings.API_KEY})
    else:
        res = requests.get(ROOT_URL+"/get_reitings?start_snap="+str(start_snap), headers = {"Http-Api-Key": settings.API_KEY})
    if res.status_code == 200:
        return res.json()
    else:
        return False
# 3. Проверка существования абитурента
# URL: /check_abit?id=:abit_id
# Метод: GET
# Параметры: обязательный abit_id - строка хэш данных абитуриента

def check_abit(id):
    res = requests.get(ROOT_URL+"/check_abit?id="+str(id), headers = {"Http-Api-Key": settings.API_KEY})
    if res.status_code == 200:
        return res.json()
    else:
        return False


