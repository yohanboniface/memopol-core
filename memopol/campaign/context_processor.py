from .models import Campaign

def campaigns(request):
    return { 'campaigns': Campaign.objects.filter(finished=None) }
