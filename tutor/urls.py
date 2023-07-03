"""tutor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from mainapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.landingpage,name="landingpage"),

# ======================= >  ADMIN SECTION  <===========================#
    path('admin_login',views.admin_login,name="admin_login"),
    path('admin_dashboard',views.admin_dashboard,name='admin_dashboard'),
    path('admin_gradeandsub',views.admin_gradeandsub,name="admin_gradeandsub"),
    path('admin_Addgrade',views.admin_Addgrade,name="admin_Addgrade"),
    path('admin_Addsubject',views.admin_Addsubject,name="admin_Addsubject"),
    path('admin_reg_accept/<int:id>',views.admin_reg_accept,name="admin_reg_accept"),
    path('admin_students',views.admin_students,name="admin_students"),
    path('admin_tutor_profileview/<int:id>',views.admin_tutor_profileview,name="admin_tutor_profileview"),
    path('admin_tutor_reject/<int:id>',views.admin_tutor_reject,name="admin_tutor_reject"),







# ======================= >  TUTOR SECTION  <===========================#
    path('tutor_login',views.tutor_login,name="tutor_login"),
    path('tutor_logout',views.tutor_logout,name="tutor_logout"),
    path('TutorSignUp',views.TutorSignUp,name="TutorSignUp"),
    path('signup_ajax',views.signup_ajax,name="signup_ajax"),
    path('email_authentication',views.email_authentication,name="email_authentication"),
    path('tutor_createprofile/<int:id>',views.tutor_createprofile,name="tutor_createprofile"),
    path('tutor_profilesave/<int:id>',views.tutor_profilesave,name="tutor_profilesave"),
    path('tutor_dashboard',views.tutor_dashboard,name='tutor_dashboard'),
    path('tutor_profile',views.tutor_profile,name="tutor_profile"),
    path('tutor_time',views.tutor_time,name="tutor_time"),

    path('save_times/<int:id>',views.save_times,name='save_times'),
    path('delete_save_time/<int:id>',views.delete_save_time,name="delete_save_time"),


    path('tutor_price',views.tutor_price,name="tutor_price"),
    path('save_price/<int:id>',views.save_price,name="save_price"),

    path('username_checker',views.username_checker,name="username_checker"),
    path('tutor_gradeandsub',views.tutor_gradeandsub,name="tutor_gradeandsub"),
    path('tutor_Gradechecker',views.tutor_Gradechecker,name="tutor_Gradechecker"),
    path('tutor_Subchecker',views.tutor_Subchecker,name="tutor_Subchecker"),


    path('tutor_addmore_grade',views.tutor_addmore_grade,name="tutor_addmore_grade"),
    path('delete_tutorgrade/<int:id>',views.delete_tutorgrade,name="delete_tutorgrade"),

    path('tutor_addmore_sub',views.tutor_addmore_sub,name="tutor_addmore_sub"),
    path('delete_tutorsub/<int:id>',views.delete_tutorsub,name="delete_tutorsub"),






















# ======================= >  STUDENT SECTION  <===========================#
    path('student_login',views.student_login,name="student_login"),
    path('student_logout',views.student_logout,name="student_logout"),
    path('student_signup',views.student_signup,name="student_signup"),
    path('student_signup_ajax',views.student_signup_ajax,name="student_signup_ajax"),
    path('student_email_authentication',views.student_email_authentication,name="student_email_authentication"),
    path('student_createprofile/<int:id>',views.student_createprofile,name="student_createprofile"),
    path('student_profilesave/<int:id>',views.student_profilesave,name="student_profilesave"),
    path('student_dashboard',views.student_dashboard,name='student_dashboard'),






]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)