from django.contrib import admin

from .models import *

admin.site.register(Tutor_Registration)
admin.site.register(Grades)
admin.site.register(Subjects)
admin.site.register(Tutor_Grades)
admin.site.register(Tutor_Subjects)
admin.site.register(Student_Registration)

admin.site.register(TimeSlot)



