from django.db import models
from datetime import datetime
from django.utils import timezone

class AndroidUrl(models.Model):
    url = models.CharField(primary_key=True, max_length=32)

class AdminInfo(models.Model):
    email = models.EmailField(primary_key=True, max_length=32)
    password = models.CharField(max_length=64, null=False)


class UserInfo(models.Model):
    # 创建学生用户模型，学号,密码,姓名,电话,邮件，5张人脸
    studentNum = models.CharField(max_length=8, primary_key=True)
    password = models.CharField(max_length=64, null=False)
    username = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=11, null=False, unique=True)
    email = models.EmailField(max_length=32, null=False, unique=True)
    # img1 = models.FileField(upload_to="train_set")
    # img2 = models.ImageField(upload_to="train_set")
    # img3 = models.ImageField(upload_to="train_set")
    # img4 = models.ImageField(upload_to="train_set")
    # img5 = models.ImageField(upload_to="train_set")
    img1 = models.CharField(max_length=255, unique=True, null=True, default=None)
    img2 = models.CharField(max_length=255, unique=True, null=True, default=None)
    img3 = models.CharField(max_length=255, unique=True, null=True, default=None)
    img4 = models.CharField(max_length=255, unique=True, null=True, default=None)
    img5 = models.CharField(max_length=255, unique=True, null=True, default=None)

    def __str__(self):
        return self.username


class TeacherInfo(models.Model):
    # 创建教师用户模型，教师编号，姓名，邮箱，电话，密码
    teacherNum = models.CharField(max_length=8, primary_key=True)
    password = models.CharField(max_length=64, null=False)
    teacherName = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=11, null=False, unique=True)
    email = models.EmailField(max_length=32, null=False, unique=True)


class CourseInfo(models.Model):
    # 创建课程表模型，课程号，课程名
    courseNum = models.CharField(max_length=7, primary_key=True)
    courseName = models.CharField(max_length=20, null=False)


class Teacher2Course(models.Model):
    course_id = models.ForeignKey('CourseInfo', null=False, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey('TeacherInfo', null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('course_id', 'teacher_id')


class choose_course(models.Model):
    # 创建选课表模型，学生表，课程表，教师表
    stu = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    teac = models.ForeignKey('TeacherInfo', on_delete=models.CASCADE)
    cour = models.ForeignKey('CourseInfo', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('stu', 'teac', 'cour')


class AttendanceInfo(models.Model):
    # 创建考勤勤信息表，考勤id，考勤时的bssid，课程id，教师id，考勤开始与结束日期时间，考勤状态(开始与结束)
    attendance_id = models.AutoField(max_length=32, primary_key=True)
    bssid = models.CharField(null=False, max_length=20)
    course_id = models.ForeignKey('CourseInfo', null=False, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey('TeacherInfo', null=False, on_delete=models.CASCADE)
    attendance_start_time = models.DateTimeField(null=False)
    attendance_end_time = models.DateTimeField(null=True, default=None)
    attendance_tag = models.CharField(null=False, max_length=1)  # 考勤标志， 1为考勤中，0为考勤结束


class attendance(models.Model):
    # 创建学生考勤记录表，学号，考勤id，信号强度，考勤状态，3张人脸
    stu = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    att = models.ForeignKey('AttendanceInfo', on_delete=models.CASCADE)
    dbm = models.CharField(null=False, max_length=20)
    tag = models.CharField(null=False, max_length=1)  # 考勤状态
    attendance_time = models.DateTimeField(null=False)
    # img1 = models.ImageField(upload_to="attendance_set/")
    # img2 = models.ImageField(upload_to="attendance_set/")
    # img3 = models.ImageField(upload_to="attendance_set/")
    img1 = models.CharField(max_length=255, null=True, unique=True, default=None)
    img2 = models.CharField(max_length=255, null=True, unique=True, default=None)
    img3 = models.CharField(max_length=255, null=True, unique=True, default=None)
    finish_tag = models.CharField(null=False, max_length=1, default=0)  # 考勤完成状态

    class Meta:
        unique_together = ('stu', 'att')


class complain(models.Model):
    # 创建学生考勤记录表，学号，考勤id，信号强度，考勤状态，3张人脸
    stu = models.ForeignKey('UserInfo', on_delete=models.CASCADE)
    att = models.ForeignKey('AttendanceInfo', on_delete=models.CASCADE)
    complain_tag = models.CharField(null=False, max_length=1, default=0)  # 申诉标志 0等待申诉，1申诉完成
    complain_text = models.CharField(max_length=255, null=True, default=None)  # 最多64个字
    return_text = models.CharField(max_length=255, null=True, default=None)  # 最多64个字，教师理由

    class Meta:
        unique_together = ('stu', 'att')
