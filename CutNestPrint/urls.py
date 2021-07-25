"""CutNestPrint URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from apps.nest.views import main_page, produce_page, fashions_page, new_item, fashions_list

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", main_page, name="main_page"),
    path("fashions/", fashions_page, name="fashions_page"),
    path("new/", new_item, name="new_item"),
    path("fashions_list/<int:fashion_id>/", fashions_list, name="fashions_list"),
    path("produce/", produce_page, name="produce_page"),
]