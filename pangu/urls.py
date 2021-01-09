"""pangu URL Configuration

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
from rest_framework import routers

from general import views

# 生成一个注册器实例对象
router = routers.DefaultRouter()

# 将需要自动生成url的接口注册
router.register(r'contact', views.ContactViewSet)
router.register(r'vendor', views.VendorViewSet)
router.register(r'order', views.OrderViewSet)
router.register(r'guarantee', views.GuaranteeViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', views.HomeView.as_view(), name='home'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('zhuceceshi/', views.Test.as_view()),  # 注册测试，访问就生成bbb-bbbb普通用户，访问前需要删除UserInformation数据表的信息
    path('test/', views.TestTemplate.as_view()),
    path('order/', include('general.urls')),
    path('contact/', include('general.urls')),
    path('search/', include('general.urls')),
    path('api/', include(router.urls))

]
