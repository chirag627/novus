"""MedicalProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.views.static import serve
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', views.index, name='index'),
                  path('login/', views.user_login, name='login'),
                  path('signup/', views.user_signup, name='signup'),
                  path('logout/', views.user_logout, name='logout'),
                  path('modules/', include('set.urls')),


                # FOR ADMIN
                  path('admin-panel/', views.admin_panel, name='admin-panel'), # admin panel
                  path('admin-panel/login/', views.admin_login, name='admin-login'), # a separate admin login page
                  path('admin-panel/logout/', views.admin_logout, name='admin-logout'), # sends to admin login page

                  path('admin-panel/list-students/', views.list_students, name="list-students"), # list of students
                  path('admin-panel/student/<int:student_pk>/', views.detail_student, name='detail-student'), # detail edit delete


              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]
