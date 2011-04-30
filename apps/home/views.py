from django.views.generic.simple import direct_to_template

def home(request):


    context = {
    }
    return direct_to_template(request, 'home.html', context)


