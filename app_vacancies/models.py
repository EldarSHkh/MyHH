from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    name = models.CharField(max_length=32)
    location = models.CharField(max_length=64)
    logo = models.ImageField(upload_to="MEDIA_COMPANY_IMAGE_DIR", default='https://place-hold.it/100x60')
    description = models.TextField()
    employee_count = models.PositiveIntegerField(null=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.CASCADE)


class Specialty(models.Model):
    code = models.CharField(max_length=60, unique=True)
    title = models.CharField(max_length=64)
    picture = models.ImageField(upload_to="MEDIA_SPECIALITY_IMAGE_DIR", default='https://place-hold.it/100x60')


class Vacancy(models.Model):
    title = models.CharField(max_length=120)
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="vacancies")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="vacancies")
    skills = models.CharField(max_length=120)
    description = models.TextField()
    salary_min = models.PositiveIntegerField()
    salary_max = models.PositiveIntegerField()
    published_at = models.DateField(default=date.today)


class Application(models.Model):
    written_username = models.CharField(max_length=64)
    written_phone = models.CharField(max_length=20)
    written_cover_letter = models.TextField()
    vacancy = models.ForeignKey(Vacancy, on_delete=models.CASCADE, related_name="applications")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")


class Resume(models.Model):
    class QualificationChoices(models.TextChoices):
        INTERN = 'intern', _('Стажер')
        JUNIOR = 'junior', _('Джуниор')
        MIDDLE = 'middle', _('Миддл')
        SENIOR = 'senior', _('Синьор')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="resume")
    name = models.CharField(max_length=120, verbose_name='Имя')
    surname = models.CharField(max_length=120, verbose_name='Фамилия')
    status = models.CharField(max_length=80, verbose_name='Готовность к работе')
    salary = models.PositiveIntegerField(verbose_name='Ожидаемое вознаграждение')
    specialty = models.ForeignKey(Specialty, on_delete=models.CASCADE, related_name="resumes",
                                  verbose_name='Специальность')
    grade = models.CharField(max_length=80, choices=QualificationChoices.choices, verbose_name='квалификация')
    education = models.TextField(verbose_name='Образование')
    experience = models.TextField(verbose_name='Опыт работы')
    portfolio = models.CharField(max_length=120, verbose_name='Ссылка на портфолио')
