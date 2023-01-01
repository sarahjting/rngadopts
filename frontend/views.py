import json
from django.shortcuts import render
from rngadopts import settings


def index(request, *args, **kwargs):
    return render(request, 'frontend/index.html', context={
        'app_url': settings.APP_URL,
        'app_flags': json.dumps({
            'adopts_creation': settings.RNGADOPTS_ADOPT_CREATION_ENABLED,
        }),
    })
