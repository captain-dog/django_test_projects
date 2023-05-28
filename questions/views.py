from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .models import Question
from .serializers import QuestionSerializer
from .services.question_services import generate_questions


class QuestionModelViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()

    def create(self, request, *args, **kwargs):
        question_num = request.data.get("question_num")
        if not question_num:
            raise APIException("give me question_num")
        if not isinstance(question_num, int):
            raise APIException("give me int question_num")

        generate_questions(question_num)
        question_qs = self.get_queryset().filter().order_by("-id")[:question_num]
        return Response(self.serializer_class(question_qs, many=True).data)
