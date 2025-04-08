from django.shortcuts import render

def show_phones(request):
    return render(request, 'start_page.html')