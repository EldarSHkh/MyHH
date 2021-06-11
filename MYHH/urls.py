from django.contrib import admin
from django.conf.urls import url
from django.contrib.auth.views import LogoutView
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from app_vacancies.views import MainView, VacanciesView, VacancyView, CompanyView, SpecializationsView, \
    SendApplicationView, \
    custom_handler404, custom_handler500, MyCompanyView, MyVacanciesView, MyVacancyView, CreateCompanyView, \
    CreateVacancyView, CreateResumeView, MyResumeView, SearchView
from MYHH.views import UserLoginView, UserSignupView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('vacancies/cat/<str:specialization>/', SpecializationsView.as_view(), name='specialization'),
    path('companies/<int:company_id>/', CompanyView.as_view(), name="company"),
    path('vacancies/<int:vacancy_id>/', VacancyView.as_view(), name="vacancy"),
    path('vacancies/', VacanciesView.as_view(), name="vacancies"),
    path('vacancies/<int:vacancy_id>/send/', SendApplicationView.as_view(), name="sendApplication"),
    path('mycompany/', MyCompanyView.as_view(), name="my_company"),
    path('mycompany/create/', CreateCompanyView.as_view(), name='create_company'),
    path('mycompany/vacancies/<vacancy_id>', MyVacancyView.as_view(), name="my_vacancy"),
    path('mycompany/vacancies/', MyVacanciesView.as_view(), name="my_vacancies"),
    path('mycompany/vacancies/create/', CreateVacancyView.as_view(), name='create_vacancy'),
    path('myresume/', MyResumeView.as_view(), name='my_resume'),
    path('myresume/create/', CreateResumeView.as_view(), name='create_resume'),
    path('search/', SearchView.as_view(), name='search')

]

urlpatterns += [
    path('signup/login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', UserSignupView.as_view(), name='signup')

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

handler404 = custom_handler404
handler500 = custom_handler500
