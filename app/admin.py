from django.contrib import admin
from .models import UserInfo, TeacherInfo, CourseInfo, choose_course, AttendanceInfo, attendance, complain


# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['studentNum', 'username', 'password', 'phone', 'email', 'img1', 'img2', 'img3', 'img4', 'img5']


class TeacherInfoAdmin(admin.ModelAdmin):
    list_display = ['teacherNum', 'password', 'teacherName', 'phone', 'email']


class CourseInfoAdmin(admin.ModelAdmin):
    list_display = ['courseNum', 'courseName']


class choose_courseAdmin(admin.ModelAdmin):
    list_display = ['stu', 'teac', 'cour']


class AttendanceInfoAdmin(admin.ModelAdmin):
    list_display = ['attendance_id', 'bssid', 'course_id', 'teacher_id', 'attendance_tag']


class attendanceAdmin(admin.ModelAdmin):
    list_display = ['stu', 'att', 'dbm', 'tag', 'img1', 'img2', 'img3', 'finish_tag']


class complainAdmin(admin.ModelAdmin):
    list_display = ['stu', 'att', 'complain_tag', 'complain_text', 'return_text']


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(TeacherInfo, TeacherInfoAdmin)
admin.site.register(CourseInfo, CourseInfoAdmin)
admin.site.register(choose_course, choose_courseAdmin)
admin.site.register(AttendanceInfo, AttendanceInfoAdmin)
admin.site.register(attendance, attendanceAdmin)
admin.site.register(complain, complainAdmin)
