from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.http import Http404, HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render, redirect, get_object_or_404

from django.views import View

from app_vacancies.form import ApplicationForm, VacancyForm, CompanyForm, ResumeForm
from app_vacancies.models import Specialty, Vacancy, Company, Application, Resume


class MainView(View):

    def get(self, request, *args, **kwargs):
        specialties = Specialty.objects.annotate(vacancies_count=Count('vacancies'))
        companies = Company.objects.annotate(vacancies_count=Count('vacancies'))
        context = {
            "specialties": specialties,
            "companies": companies
        }

        return render(request, 'index.html', context=context)


class VacanciesView(View):

    def get(self, request, *args, **kwargs):
        vacancies = Vacancy.objects.all()
        context = {
            "vacancies": vacancies
        }

        return render(request, 'vacancies.html', context=context)


class CompanyView(View):

    def get(self, request, company_id, *args, **kwargs):
        company = get_object_or_404(Company, id=company_id)
        vacancies = Vacancy.objects.filter(company=company)
        context = {
            'company': company,
            'vacancies': vacancies,
        }

        return render(request, 'company.html', context=context)


class VacancyView(View):

    def get(self, request, vacancy_id, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        form = ApplicationForm()
        context = {
            'vacancy': vacancy,
            'form': form
        }

        return render(request, 'vacancy.html', context=context)


class SpecializationsView(View):

    def get(self, request, specialization, *args, **kwargs):
        specialization = get_object_or_404(Specialty, code=specialization)
        vacancies = Vacancy.objects.filter(specialty=specialization)
        context = {
            'specialization': specialization,
            'vacancies': vacancies,
        }

        return render(request, 'vacancies.html', context=context)


class SendApplicationView(View):

    def get(self, request, vacancy_id, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, id=vacancy_id)
        try:
            Application.objects.filter(vacancy=vacancy, user_id=request.user.id)
        except Vacancy.DoesNotExist:
            raise Http404

        context = {
            'vacancy': vacancy
        }

        return render(request, 'sent.html', context=context)

    def post(self, request, vacancy_id, *args, **kwargs):
        application_data = ApplicationForm(request.POST).save(commit=False)
        application_data.vacancy = Vacancy.objects.get(id=vacancy_id)
        application_data.user = User.objects.get(id=request.user.id)
        application_data.save()

        return redirect("sendApplication", vacancy_id)


class MyCompanyView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        if not company:
            return render(request, 'company-create.html')
        form = CompanyForm(instance=company)

        context = {
            'form': form,
        }

        return render(request, 'company-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        if not company:
            return render(request, 'company-create.html')
        CompanyForm(request.POST, request.FILES, instance=company).save()

        return redirect('my_company')


class CreateCompanyView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = CompanyForm()
        context = {
            'form': form,
        }

        return render(request, 'company-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        company_data = CompanyForm(request.POST, request.FILES, instance=company).save()
        company_data.owner = User.objects.get(id=request.user.id)
        company_data.save()

        return redirect('my_company')


class MyVacanciesView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        if not company:
            return redirect('my_company')
        vacancies = Vacancy.objects.filter(company=company).annotate(applications_count=Count('applications'))
        context = {
            'vacancies': vacancies,
        }

        return render(request, 'vacancy_list.html', context=context)


class CreateVacancyView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        if not company:
            return redirect('my_company')
        form = VacancyForm()
        context = {
            'form': form,
        }

        return render(request, 'vacancy-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        if not company:
            return redirect('my_company')
        vacancy_data = VacancyForm(request.POST).save(commit=False)
        vacancy_data.company = company
        vacancy_data.save()

        return redirect('main')


class MyVacancyView(LoginRequiredMixin, View):

    def get(self, request, vacancy_id, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        if not company:
            return redirect('my_company')
        vacancy = get_object_or_404(Vacancy, company=company, id=vacancy_id)
        form = VacancyForm(instance=vacancy)
        applications = Application.objects.filter(vacancy__id=vacancy_id)
        context = {
            'form': form,
            'applications': applications,
        }

        return render(request, 'vacancy-edit.html', context=context)

    def post(self, request, vacancy_id, *args, **kwargs):
        company = Company.objects.filter(owner__id=request.user.id).first()
        if not company:
            return redirect('my_company')
        try:
            vacancy = Vacancy.objects.get(company=company, id=vacancy_id)
        except Vacancy.DoesNotExist:
            return redirect('my_vacancies')
        VacancyForm(request.POST, instance=vacancy).save()

        return redirect('my_vacancy', vacancy_id)


class MyResumeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        resume = Resume.objects.filter(user__id=request.user.id).first()
        if not resume:
            return render(request, 'resume-create.html')
        form = ResumeForm(instance=resume)
        context = {
            'form': form,
        }
        return render(request, 'resume-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        resume = Resume.objects.filter(user__id=request.user.id).first()
        if not resume:
            return render(request, 'resume-create.html')
        ResumeForm(request.POST, instance=resume).save()

        return redirect('my_resume')


class CreateResumeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'form': ResumeForm(),
        }

        return render(request, 'resume-edit.html', context=context)

    def post(self, request, *args, **kwargs):
        resume_data = ResumeForm(request.POST).save(commit=False)
        resume_data.user = User.objects.get(id=request.user.id)
        resume_data.save()

        return redirect('my_resume')


class SearchView(View):

    def get(self, request, *args, **kwargs):
        target_search = request.GET['s']
        vacancies = Vacancy.objects.filter(Q(title__icontains=target_search) | Q(description__icontains=target_search))
        context = {
            "vacancies": vacancies
        }

        return render(request, 'search.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound('404')


def custom_handler500(request):
    return HttpResponseServerError('500')
