import json

import requests

from questions.models import Question
from questions.serializers import QuestionSerializer
from loguru import logger


def get_questions_from_jservice(question_num: int) -> list[dict]:
    """Получает question_num вопросов из сервисе jservice
    Поднимает исключение если сервис не ответил"""
    response = requests.get(f"https://jservice.io/api/random?count={question_num}")
    assert response.status_code == 200

    data = json.loads(response.text)
    for question in data:
        question["question_id"] = question.get('id')
    return data


def create_question(data) -> Question:
    """Создаёт инстанс вопроса с предварительной валидацией данных"""
    serializer = QuestionSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    return Question.objects.create(**serializer.validated_data)


def find_new_unique_question(db_question_ids: list[int]) -> Question:
    """
    Пытается найти такой вопрос, айди которого нет в списке db_question_ids.
    Пытается number_of_tries раз после чего рейзит исключение
    """
    logger.debug(f"Starting searching a new...")

    number_of_tries = 10

    for i in range(number_of_tries):
        new_question_data = get_questions_from_jservice(question_num=1)[0]
        if not (new_question_data.get('id') in db_question_ids):
            logger.debug(f"found new unique question {new_question_data.get('id')}!")
            new_question = create_question(data=new_question_data)
            return new_question
    else:
        logger.warning(f"question {new_question_data.get('id')} exists in db, i'll try again")


    logger.error('too many requests made')
    raise Exception


def generate_questions(question_num: int) -> None:
    """
    Создает в базе данных уникальные вопросы на основе тех, что были получены от сервиса
    https://jservice.io/api/random
    """

    questions_from_jservice: list[dict] = get_questions_from_jservice(question_num=question_num)
    db_question_ids: list[int] = list(Question.objects.all().values_list('question_id', flat=True))
    for question in questions_from_jservice:
        current_question_id = question.get('id')
        if current_question_id in db_question_ids:
            logger.warning(f"question {current_question_id} exists")

            new_question = find_new_unique_question(db_question_ids)
            db_question_ids.append(new_question.question_id)
            continue

        else:
            logger.debug('Creating new unique question')
            db_question_ids.append(current_question_id)
            create_question(data=question)
