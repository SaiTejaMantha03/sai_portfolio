from django.http import HttpResponsePermanentRedirect
from django.views.generic import RedirectView

class DomainRedirectView(RedirectView):
    """
    View to handle domain redirects
    """
    permanent = True
    
    def get_redirect_url(self, *args, **kwargs):
        # Always redirect to saiwith.tech
        protocol = 'https' if self.request.is_secure() else 'http'
        return f"{protocol}://saiwith.tech{self.request.get_full_path()}"