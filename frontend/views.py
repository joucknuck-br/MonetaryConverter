from django.shortcuts import render


def conversion_form(request):
    return render(request, 'conversion_form.html')
