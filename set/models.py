from django.db import models
from django.contrib.auth.models import User


class Module(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Set(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name


class Question(models.Model):
    ANS_TYPE_CHIOICES = (
        (1, "Normal"),
        (2, "Abnormal")
    )
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    dcom_file = models.FileField(upload_to="dcom_files")
    ans_type = models.IntegerField(choices=ANS_TYPE_CHIOICES, default=1)
    ans_text = models.CharField(max_length=1000, blank=True)

    def get_file_url(self):
        return self.dcom_file.url


class AttemptedSet(models.Model):
    set = models.ForeignKey(Set, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    attempted_on = models.DateTimeField(auto_now_add=True)

    time_taken = models.CharField(max_length=64, blank=True)
    num_answered = models.IntegerField(blank=True, null=True)
    num_questions = models.IntegerField(blank=True, null=True)
    num_correct = models.IntegerField(blank=True, null=True)

    is_evaluated = models.BooleanField(default=False)

    def __str__(self):
        return self.set.name + " by " + self.user.username


class Response(models.Model):
    ANS_TYPE_CHIOICES = (
        (1, "Normal"),
        (2, "Abnormal")
    )
    attempt = models.ForeignKey(AttemptedSet, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    ans_type = models.IntegerField(choices=ANS_TYPE_CHIOICES, default=1)
    ans_text = models.CharField(max_length=1000, blank=True, null=True)

    # for evaluating

    is_correct = models.BooleanField(default=False)
