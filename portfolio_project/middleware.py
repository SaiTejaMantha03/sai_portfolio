from django.http import HttpResponsePermanentRedirect
from django.utils.deprecation import MiddlewareMixin

class DomainRedirectMiddleware(MiddlewareMixin):
    """
    Middleware to redirect home.saiwith.tech to saiwith.tech
    """
    def process_request(self, request):
        host = request.get_host().lower()
        
        # Redirect home.saiwith.tech to saiwith.tech
        if host == 'home.saiwith.tech':
            protocol = 'https' if request.is_secure() else 'http'
            new_url = f"{protocol}://saiwith.tech{request.get_full_path()}"
            return HttpResponsePermanentRedirect(new_url)
        
        return None