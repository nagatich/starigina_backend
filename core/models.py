from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    answer = models.CharField(max_length=150, verbose_name='Ответ')
    score = models.IntegerField(verbose_name='Балл')
    a = models.FloatField(default=0)
    b = models.FloatField(default=0)
    c = models.FloatField(default=0)
    pov = models.FloatField(default=0)
    shel = models.FloatField(default=0)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.answer

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    question_text = models.CharField(max_length=150, verbose_name='Вопрос')
    answers = models.ManyToManyField(Answer, related_name='question_answer', blank=True, verbose_name='Ответы')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question_text

class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    test_name = models.CharField(max_length=150, verbose_name='Название теста')
    questions = models.ManyToManyField(Question, blank=True, verbose_name='Вопросы')

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'

    def __str__(self):
        return '{} - {}'.format(self.user, self.test_name)

class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос')
    answers = models.ManyToManyField(Answer, verbose_name='Ответы')

    class Meta:
        verbose_name = 'Ответ студента'
        verbose_name_plural = 'Ответы студентов'

    def __str__(self):
        return '{} - {}'.format(self.student, self.question)

    @property
    def total_score(self):
        total = 0
        for answer in self.answers.all():
            total += answer.score
        return total

class StudentTest(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE, null=True, verbose_name='Пользователь')
    test = models.ForeignKey(Test, on_delete=models.CASCADE, verbose_name='Тест')
    questions = models.ManyToManyField(StudentAnswer, verbose_name='Вопросы')
    passed = models.BooleanField(default=False, verbose_name='Выполнено')

    class Meta:
        verbose_name = 'Тест студента'
        verbose_name_plural = 'Тесты студентов'

    def __str__(self):
        return '{} - {}'.format(self.student, self.test)