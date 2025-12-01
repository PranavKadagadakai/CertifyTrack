"""
URL configuration for CertifyTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=False)

# Custom view to serve certificate files with framing allowed
from django.http import HttpResponse
from django.views.decorators.http import require_GET

@require_GET
def serve_certificate(request, path):
    from django.conf import settings
    from django.http import Http404
    import os

    # Only allow certificate files
    if not path.startswith('certificates/'):
        raise Http404("Access denied")

    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # Security check
    if not os.path.exists(file_path) or not os.path.isfile(file_path):
        raise Http404("File not found")

    try:
        with open(file_path, 'rb') as f:
            response = HttpResponse(f.read(), content_type='application/pdf')
            # Explicitly allow framing for certificate previews
            response['X-Frame-Options'] = 'ALLOWALL'
            return response
    except IOError:
        raise Http404("File not readable")

# Add custom URL pattern for certificates
from django.urls import path
urlpatterns += [
    path('media/certificates/<path:path>', serve_certificate, name='serve_certificate'),
]
