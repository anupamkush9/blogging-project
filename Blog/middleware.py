# middleware.py

class CaptureClientIPMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to capture the client IP before the view is called.
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = ""
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        
        # Attach the client's IP address to the request object
        request.client_ip = ip

        # Call the next middleware or view
        response = self.get_response(request)

        # Code to be executed after the view is called.
        return response
