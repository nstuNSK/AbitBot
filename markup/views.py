from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import authenticate
from django.db.utils import IntegrityError
from django.db.models import Max
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_payload_handler, jwt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.contrib.staticfiles import finders
from django.http import HttpResponse
from django.template import Context, loader
from administrator.models import User
from administrator.serializers import UserSerializer
from administrator.views import getJWT
from .models import Question, Mark, User_Question, Question_Mark
from .utils import ResponseThen


from AbitBot import settings
import pandas as pd

import random
from rest_framework.authentication import SessionAuthentication, BasicAuthentication 

class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return None

def index(request):
	if request.method == "GET":
	    template=loader.get_template("index2.html")
	    return HttpResponse(template.render())

class LoginView(APIView):
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication,JSONWebTokenAuthentication)

    def post(self, request):
        data = request.data
        if "login" in data and "password" in data:
            try:
                user = User.objects.get(login = data["login"])
                if user.check_password(data["password"]):
                    jwt = getJWT(user)
                    serializer = UserSerializer(user)
                    res = {"jwt": jwt,
                           "is_admin": user.isAdmin}
                    res.update(serializer.data)
                    return Response(data = res, status = status.HTTP_200_OK)
                else:
                    return Response({"descr": "wrong login or password"}, status = status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)

class Class_Add(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def check_question(self, question):
        qs = User_Question.objects.filter(question=question)
        if len(qs)>=3:
            marks = []
            for q in qs:
                marks.append(q.mark.name)
            unique_marks = list(set(marks))
            max_count = 0
            max_count_mark = ""
            for m in unique_marks:
                temp = marks.count(m)
                if temp > max_count:
                    max_count = temp
                    max_count_mark = m
            if max_count/len(marks) >= 2/3:
                return (True, max_count_mark)
        return (False, None)


    def add_class(self, q_id, mark_id, user):
        question = Question.objects.get(id=q_id)
        mark = Mark.objects.get(id=mark_id)
        User_Question.objects.create(user=user, question=question, mark=mark)
        checked = self.check_question(question)
        if checked[0]:
            mark_name = checked[1]
            t_mark = Mark.objects.get(name=mark_name)
            Question_Mark.objects.create(question=question, mark=t_mark)
        

    
    def post(self, request):
        user = request.user
        if "mas" in request.data:
            try:
                questions = request.data["mas"]
                for q in questions:
                    self.add_class(q['id'], q['type'], user)
                res = {"status": "success", "status_code": "200"}
                return Response(data = res, status = status.HTTP_200_OK)
            except:
                raise
                res = {"status": "failed", "status_code": "400"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        else:
            res = {"status": "failed", "status_code": "400"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)


class Get_Questions(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def get_statistics(self, user):
        #itsnewfile!
        local_stat = len(User_Question.objects.filter(user=user))
        global_stat = len(Question_Mark.objects.all())
        total = len(Question.objects.all())
        marks = Mark.objects.all()
        local_marks_stat = []
        for m in marks:
            temp = {"mark_id": m.id, "mark_name": m.name, "priority": m.priority, "count": len(User_Question.objects.filter(mark=m, user=user))}
            local_marks_stat.append(temp)
        global_marks_stat = []
        for m in marks:
            temp = {"mark_id": m.id, "mark_name": m.name, "priority": m.priority, "count": len(Question_Mark.objects.filter(mark=m))}
            global_marks_stat.append(temp)

        return {"markup_stat": {"local": local_stat, "global": global_stat, "total": total},
                "marks_stat":  {"local": local_marks_stat, "global": global_marks_stat}}
    
    def filter_question(self, question, user, unavailable_questions, user_questions):
        for q in unavailable_questions:
            if q.question == question:
                return False
        for q in user_questions:
            if q.question == question:
                return False
        return True
        
    def get_questions(self, user, sample_size=10):
        all_questions = Question.objects.all()
        user_questions = User_Question.objects.filter(user=user)
        unavailable_questions = Question_Mark.objects.all()
        questions = []

        for q in all_questions:
            if self.filter_question(q, user, unavailable_questions, user_questions):
                questions.append(q)
            if len(questions) == sample_size:
                break
        return questions
    
    def convert_to_json(self, questions):
        res = []
        for q in questions:
            temp = {"id": q.id,
                    "question":q.question}
            res.append(temp)
        return res
    
    def get_marks(slef):
        marks = Mark.objects.all()
        res = []
        for m in marks:
            temp = {
                "id": m.id,
                "name": m.name,
                "priority": m.priority
            }
            res.append(temp)
        return res

    def get_admin_stat(self, user):
        if user.isAdmin:
            res = []
            accounts = User.objects.filter(id__gt=2)
            print(accounts)
            for acc in accounts:
                count = len(User_Question.objects.filter(user=acc))
                print(count)
                res.append({"name": acc.login, "count": count})
            return res
        else:
            return []
    def post(self, request):
        user = request.user
        stat = self.get_statistics(user)
        qs = self.get_questions(user)
        q_json = self.convert_to_json(qs)
        marks = self.get_marks()
        admin_stat = self.get_admin_stat(user)
        res = {"stat": stat, "questions": q_json, "marks": marks, "is_admin": user.isAdmin, "admin_stat": admin_stat}
        return Response(data = res, status = status.HTTP_200_OK)

class SetPriority(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def set_priority_for_one(self, id, priority):
        try:
            m = Mark.objects.get(id=id)
            m.priority = priority
            m.save()
            return True
        except:
            return False

    def set_priority(self, marks):
        res = {"res": []}
        for m in marks:
            if self.set_priority_for_one(m['id'], m['priority']):
                res['res'].append({"mark_id": m['id'], "status": True})
            else:
                res['res'].append({"mark_id": m['id'], "status": False})
        return res


    def post(self, request):
        user = request.user
        if user.isAdmin:
            marks = request.data['marks']
            res = self.set_priority(marks)
            return Response(data = res, status = status.HTTP_200_OK)
        else:
            res = {"status": "permission denied"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

class DeleteMark(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def post(self, request):
        user = request.user
        mark_id = request.data['id']
        if user.isAdmin:
            try:
                mark = Mark.objects.get(id=mark_id)
                mark.delete()
                return Response(status = status.HTTP_200_OK)
            except:
                return Response(status = status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status = status.HTTP_400_BAD_REQUEST)


class Marks(APIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser,)
    authentication_classes = (CsrfExemptSessionAuthentication, JSONWebTokenAuthentication)

    def add_mark(self, mark):
        max_id = Mark.objects.aggregate(Max("id"))['id__max']
        max_prior = Mark.objects.aggregate(Max("priority"))['priority__max']
        try:
            if "priority" in mark:
                Mark.objects.create(id=int(max_id)+1, name=mark['name'], priority=int(mark['priority']))
            else:
                Mark.objects.create(id=int(max_id)+1, name=mark['name'], priority=int(max_prior)+1)
            return True
        except IntegrityError:
            return False
    
    def get_marks(self):
        ms = Mark.objects.all()
        res = {"marks": []}
        for m in ms:
            temp = {
                "id": m.id,
                "name": m.name,
                "priority": m.priority
            }
            res['marks'].append(temp)
        return res
    
    def get(self, requset):
        res = self.get_marks()
        return Response(data = res, status = status.HTTP_200_OK)

    
    def post(self, request):
        user = request.user
        if user.isAdmin:
            if self.add_mark(request.data['mark']):
                return Response(status = status.HTTP_200_OK)
            else:
                res = {"status": "error"}
                return Response(data = res, status = status.HTTP_400_BAD_REQUEST)
        else:
            res = {"status": "permission denied"}
            return Response(data = res, status = status.HTTP_400_BAD_REQUEST)

# class SecretDB(APIView):
#     permission_classes = (AllowAny,)
#     parser_classes = (JSONParser,)
#     authentication_classes = (CsrfExemptSessionAuthentication,JSONWebTokenAuthentication)

#     def fill_question_table(self, offset):
#         df = pd.read_csv(settings.DATA_CSV_PATH)
#         i = 0
#         for index, row in df.iterrows():
#             if i >= offset:
#                 question = row['q']
#                 answer = row['a']
#                 Question.objects.create(question=question, answer=answer)
#             else:
#                 i += 1
    
#     def fill_mark_table(self):
#         data = [
#             'Прием документов',
#             'Порядок приема',
#             'Направления подготовки',
#             'Начисление стипендии',
#             'Вступительные экзамены',
#             'ЕГЭ',
#             'Перевод из других ВУЗов',
#             'Общежития',
#             'Списки поступающих',
#             'Приказы о зачислении',
#             'Военная кафедра',
#             'Трудоустройство',
#             'Личный кабинет',
#             'Контакты',
#             'Несколько вопросов',
#             'Мусор'
#         ]
#         for i in range(1, len(data)+1):
#             Mark.objects.create(id=i, name=data[i-1])
    
#     def post(self, request):
#         data = request.data
#         if "secret" in data and data['secret'] == settings.SECRET_DB:
#             if "question_table" in data['tables']:
#                 res = {"status": "start filling question table"}
#                 return ResponseThen(data = res, then_callback = self.fill_question_table, arg =data['offset'], status = status.HTTP_200_OK)
#             if "mark_table" in data['tables']:
#                 res = {"status": "start filling mark table"}
#                 return ResponseThen(data = res, then_callback = self.fill_mark_table, status = status.HTTP_200_OK)
#             res = {"success": True}
        
#         if "set_default_priority" in data:
#             marks = Mark.objects.all()
#             for m in marks:
#                 m.priority = m.id
#                 m.save()
#             res = {"marks": []}
#             for m in marks:
#                 res['marks'].append([m.id, m.name, m.priority])
#             return Response(data = res, status = status.HTTP_200_OK)
            
#         if "test" in data:
#             qs = Question.objects.all()
#             ms = Mark.objects.all()
#             res = {
#                     "questions": [],
#                     "marks": []
#                    }
#             for i in range(10):
#                 res["questions"].append(qs[i].question)
#             for m in ms:
#                 res['marks'].append([m.id, m.name, m.priority])
#             return Response(data = res, status = status.HTTP_200_OK)
#         if "clear" in data:
#             Question.objects.all().delete()
#             return Response(status = status.HTTP_200_OK)
#         if "test_M" in data:
#             ms = Mark.objects.all()
#             res = {
#                     "marks": []
#                   }
#             for m in ms:
#                 res['marks'].append({"id": m.id, "name": m.name})
#             return Response(data = res, status = status.HTTP_200_OK)
#         if "test_UQ" in data:
#             items = User_Question.objects.all()
#             res = []
#             for i in items:
#                 res.append({"user_id": i.user.id, "question_id": i.question.id, "mark_id": i.mark.id})
#             return Response(data = res, status = status.HTTP_200_OK)
#         if "clear_UQ" in data:
#             User_Question.objects.all().delete()
#             return Response(status = status.HTTP_200_OK)
#         if "test_QM" in data:
#             items = Question_Mark.objects.all()
#             res = []
#             for i in items:
#                 res.append({"mark_id": i.mark.id, "question_id": i.question.id})
#             return Response(data = res, status = status.HTTP_200_OK)
#         if "clear_QM" in data:
#             Question_Mark.objects.all().delete()
#             return Response(status = status.HTTP_200_OK)
#         if "add_mark" in data:
#             Mark.objects.create(id=17, name="Подача заявления о согласии")
#             return Response(status = status.HTTP_200_OK)