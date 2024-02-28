from django.urls import path

from frontend.views import conversion_form

urlpatterns = [
    path('conversion_form/', conversion_form, name='conversion_form'),
]