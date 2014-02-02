from django.shortcuts import render
from rest_framework.reverse import reverse
from django.templatetags.static import static

def api(request):
    tenant = request.tenant
    api_url = reverse('timetable', request=request)
    root_url = request.build_absolute_uri('/')
    script_url = request.build_absolute_uri(static('stables-timetable.js'))
    return render(request, 'api.html', {
        'tenant': tenant,
        'api_url': api_url,
        'root_url': root_url,
        'script_url': script_url,
        })
