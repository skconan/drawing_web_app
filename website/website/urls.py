"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from drawing import views as views_drawing
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views_drawing.index, name="index"),
    path('index/', views_drawing.index, name="index"),
    path('reset_is_label/', views_drawing.reset_is_label, name="reset_is_label"),
    path('label/', views_drawing.label, name="label"),
    path('upload/', views_drawing.upload, name="upload"),
    path('select_mission/', views_drawing.select_mission, name="select_mission"),
    path('dataset/<int:page>', views_drawing.dataset, name="dataset"),
    path('dataset/', views_drawing.dataset, name="dataset"),
    path('videos/<int:page>', views_drawing.videos, name="videos"),
    path('videos/', views_drawing.videos, name="videos")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)   