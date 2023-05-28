import json

import requests
from .serializers import QuestionSerializer

from django.test import TestCase
from loguru import logger


from questions.models import Question


class QuestionTest(TestCase):
    def setUp(self) -> None:
        q1: Question = Question.objects.create(question="hi?",
                                               answer="hi!",
                                               question_id=1,
                                               created_at="2023-05-27")

    def test_question(self):
        # logger.debug(Question.objects.all().first().question_text)
        response = requests.get("https://jservice.io/api/random?count=3")
        data = json.loads(response.text)
        for question in data:
            question["question_id"]=question.get('id')
            serializer = QuestionSerializer(data=question)
            serializer.is_valid(raise_exception=True)
            Question.objects.create(**serializer.validated_data)
        qs = Question.objects.all()
        self.assertEqual(len(qs), 4)