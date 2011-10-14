from django.contrib import admin

from . models import Company, Speaker, Lecture, Partner, PartnerSection


class LectureAdmin(admin.ModelAdmin):
    list_display_links = ('title',)
    list_display = ('start', 'start_date', 'is_brake', 'start_time', 'end', 'title', 'speaker')
    list_editable = ('start',)

    def start_date(self, model):
        return model.start.date()

    def start_time(self, model):
        return model.start.time()


admin.site.register(Company)
admin.site.register(Speaker)
admin.site.register(Lecture, LectureAdmin)
admin.site.register(Partner)
admin.site.register(PartnerSection)