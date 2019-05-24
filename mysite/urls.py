"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^login/', views.login, name='login'),
    url(r'^register/', views.register, name='register'),
    url(r'^register_verify/', views.register_verify),
    url(r'^index/', views.index),
    url(r'^logout/', views.logout),
    url(r'^check/', views.check),
    # url(r'^classManage/',views.classManage),
    # url(r'^edit_class',views.edit_class),
    # url(r'^delete_class',views.delete_class),
    # url(r'^add_class/',views.add_class),
    # url(r'^majorManage/',views.majorManage),
    # url(r'^add_major/',views.add_major),
    # url(r'^delete_major',views.delete_major),
    # url(r'^edit_major/',views.edit_major),
    # url(r'^memberManage/',views.member_manage),
    # url(r'^delete_member',views.delete_member),
    # url(r'^edit_member',views.edit_member),
    # url(r'^total',views.total),
    # url(r'^sign_solve/',views.total),
    # url(r'^notice/',views.notice),
    # url(r'^noticeManage/',views.noticeManage),
    # url(r'^leave/',views.leave),
    # url(r'^exam/',views.exam),
    # url(r'^exam_manage/',views.exam_manage),
    url(r'^forget_password/', views.forget_password),
    url(r'^personal_details/', views.personal_details),
    url(r'^contact_us/', views.contact_us),
    url(r'^teacher_contact_us/', views.teacher_contact_us),
    url(r'^face_upload/', views.face_upload),
    url(r'^face_gallery/', views.face_gallery),
    url(r'^create_course/', views.create_course),
    url(r'^teacher_index/', views.teacher_index),
    url(r'^teacher_check/', views.teacher_check),
    url(r'^admin_index/', views.admin_index),
    url(r'^admin_check/', views.admin_check),
    url(r'^operation/', views.operation),
    url(r'^add_UserInfo_2db/', views.add_UserInfo_2db),
    url(r'^student2course_connection/', views.student2course_connection),
    url(r'^chosen_course/', views.chosen_course),
    url(r'^add_UserInfo_img_2db/', views.add_UserInfo_img_2db),
    url(r'^teacher_details/', views.teacher_details),
    url(r'^teacher_login/', views.teacher_login),
    url(r'^admin_login/', views.admin_login),
    url(r'^watch_students/', views.watch_students),
    url(r'^decode/', views.decode),
    # url(r'^search_student_face/', views.search_student_face),
    # url(r'^human_face/', views.human_face),
    url(r'^watch_face/', views.watch_face),
    url(r'^stu_upload/', views.stu_upload),
    url(r'^teacher_manage_atten/', views.teacher_manage_atten),
    url(r'^teacher_atten_course/', views.teacher_atten_course),
    url(r'^create_two_teachers/', views.create_two_teachers),
    url(r'^upload_atten_demo/', views.upload_atten_demo),
    url(r'^anti_proof_dataset/', views.anti_proof_dataset),
    url(r'^anti_proof_train/', views.anti_proof_train),
    url(r'^students_anti_proof/', views.students_anti_proof),
    url(r'^train/', views.train),
    url(r'^face_recognition_students/', views.face_recognition_students),
    url(r'^course_verify/', views.course_verify),
    url(r'^wifi_finger/', views.wifi_finger),
    url(r'^manage_student_account/', views.manage_student_account),
    url(r'^manage_teacher_account/', views.manage_teacher_account),
    url(r'^delete_attendance/', views.delete_attendance),
    url(r'^delete_course/', views.delete_course),
    url(r'^delete_choose_course/', views.delete_choose_course),
    url(r'^stu_check_atten/', views.stu_check_atten),
    url(r'^attendance_complain/', views.attendance_complain),
    url(r'^complain_process/', views.complain_process),
]

# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
