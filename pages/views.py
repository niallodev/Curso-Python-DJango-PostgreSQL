from django.shortcuts import render
from memberships.models import Membership
from django.contrib.auth.decorators import login_required



def index(request):
    return render(request, 'pages/index.html', {'show_footer': True})

def about(request):
    return render(request, 'pages/about.html', {'show_footer': True})


@login_required
def services(request):
    membresia = Membership.objects.filter(is_active=True) 
    return render(request, 'pages/services.html', {'membresias': membresia, 'show_footer': True})


def contact(request):
    return render(request, 'pages/contact.html', {'show_footer': True})
