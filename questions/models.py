from django.db import models


class Question(models.Model):
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    question_id = models.IntegerField()
    question = models.TextField(verbose_name="Текст вопроса")
    answer = models.TextField(verbose_name="Ответ")
    created_at = models.DateTimeField()

    def __str__(self):
        return f"{self.question}"
