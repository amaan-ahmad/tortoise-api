"""tortoise URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework import routers
from quickstart import views

router = routers.DefaultRouter()

urlpatterns = [
    path('api/users', views.UsersView.as_view()),
    path('api/brands', views.BrandsView.as_view()),
    path('api/brands/<int:brand_id>/plans', views.PlansView.as_view()),
    path('api/plans', views.PlansView.as_view()),
    path('api/plans/<int:plan_id>/promote', views.PromotionsView.as_view()),
    path('api/plans/<int:plan_id>/enroll', views.EnrollView.as_view()),
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
]
