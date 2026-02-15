from django.db import models

# Create your models here
class login_tb(models.Model):
    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    usertype=models.CharField(max_length=200)

class company_tb(models.Model):
    name=models.CharField(max_length=200)
    email=models.CharField(max_length=200)
    contact=models.CharField(max_length=200)
    lisence=models.CharField(max_length=200)
    image=models.CharField(max_length=700)
    latitude=models.CharField(max_length=200)
    longitude=models.CharField(max_length=200)
    LOGIN=models.ForeignKey(login_tb,default=1,on_delete=models.CASCADE)

class user_tb(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    place = models.CharField(max_length=200)
    pin = models.CharField(max_length=200)
    post = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    contact = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    LOGIN = models.ForeignKey(login_tb, default=1, on_delete=models.CASCADE)


class vacancy_tb(models.Model):
    vacancy_type=models.CharField(max_length=200)
    job_title=models.CharField(max_length=200)
    job_requirement=models.CharField(max_length=200)
    apply_date=models.CharField(max_length=200)
    salary=models.CharField(max_length=200)
    cuttoff = models.CharField(max_length=100, default=1)
    COMPANY=models.ForeignKey(company_tb,default=1,on_delete=models.CASCADE)

class question_tb(models.Model):
    answer=models.CharField(max_length=200)
    question=models.CharField(max_length=200)
    option_A=models.CharField(max_length=200)
    option_B=models.CharField(max_length=200)
    option_C=models.CharField(max_length=200)
    option_D=models.CharField(max_length=200)
    VACENCY=models.ForeignKey(vacancy_tb, default=1, on_delete=models.CASCADE)

class chat_tb(models.Model):
    chat=models.CharField(max_length=200)
    date=models.CharField(max_length=200)
    type=models.CharField(max_length=200)
    COMPANY=models.ForeignKey(company_tb,default=1,on_delete=models.CASCADE)
    USER = models.ForeignKey(user_tb, default=1, on_delete=models.CASCADE)

class review_tb(models.Model):
    review = models.CharField(max_length=200)
    USER = models.ForeignKey(user_tb, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    COMPANY = models.ForeignKey(company_tb, default=1, on_delete=models.CASCADE)

class candidate_tb(models.Model):
    VACENCY=models.ForeignKey(vacancy_tb, default=1, on_delete=models.CASCADE)
    USER = models.ForeignKey(user_tb, default=1, on_delete=models.CASCADE)
    date = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    exam_date = models.CharField(max_length=200)
    exam_time = models.CharField(max_length=200)
    interview_date= models.CharField(max_length=200)
    interview_time= models.CharField(max_length=200)
    no_of_unknown_person = models.CharField(max_length=100)
    multiple_person = models.CharField(max_length=100)

class exam_tb(models.Model):
    CANDIDATE=models.ForeignKey(candidate_tb, default=1, on_delete=models.CASCADE)
    mark= models.CharField(max_length=200)


class test_result(models.Model):
    USER = models.ForeignKey(user_tb, default=1, on_delete=models.CASCADE)
    QUESTION = models.ForeignKey(question_tb, default=1, on_delete=models.CASCADE)
    mark = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    date = models.CharField(max_length=200)


class camera(models.Model):
    camera_number = models.CharField(max_length=20)
    CANDIDATE = models.ForeignKey(user_tb, on_delete=models.CASCADE, default=1)

class emotions(models.Model):
    emotions = models.CharField(max_length=100)
    CANDIDATE = models.ForeignKey(user_tb, on_delete=models.CASCADE, default=1)