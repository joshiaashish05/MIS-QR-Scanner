from django.utils import timezone

class IndianTimeZoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        timezone.activate('Asia/Kolkata')
        return self.get_response(request)