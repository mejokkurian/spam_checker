from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from .import views

urlpatterns = [
   path('UserRegistration',views.UserRegistration.as_view(),name='UserRegistration'),
   path('',views.UserLogin.as_view(),name='UserLogin'),
   path('import_contact',views.import_contact.as_view(),name='import_contact'),
   path('UserSearchView',views.UserSearchView.as_view(),name='UserSearchView'),
   path('SpamReport',views.SpamReport.as_view(),name='SpamReport'),
   path('Emailadding',views.Emailadding.as_view(),name='Emailadding'),
]
