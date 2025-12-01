from django.conf import settings


class MediaFrameOptionsMiddleware:
    """
    Middleware to remove X-Frame-Options header for media files to allow
    certificate previews in iframes for mentor dashboard.
    Runs after django.middleware.clickjacking.XFrameOptionsMiddleware.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Remove X-Frame-Options header for media files to allow iframes
        if hasattr(request, 'path') and request.path.startswith(settings.MEDIA_URL):
            if 'X-Frame-Options' in response:
                del response['X-Frame-Options']

        return response
