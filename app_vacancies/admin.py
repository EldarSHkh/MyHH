from django.contrib import admin
from .models import Vacancy, Company, Specialty, Application, Resume


class VacancyAdmin(admin.ModelAdmin):
    list_display = ('title',)


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name',)


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('written_username', 'vacancy')


class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('title',)
    pass


class ResumeAdmin(admin.ModelAdmin):
    list_display = ('user',)
    pass


admin.site.register(Vacancy, VacancyAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Application, ApplicationAdmin)
admin.site.register(Specialty, SpecialtyAdmin)
admin.site.register(Resume, ResumeAdmin)
