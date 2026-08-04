from rest_framework.throttling import SimpleRateThrottle

class LoginThrottle(SimpleRateThrottle):
    scope = "login"

    def get_cache_key(self, request, view):
        username = request.data.get("username")

        if username:
            ident = username.lower()
        else:
            ident = self.get_ident(request) 

        return self.cache_format % {
            "scope": self.scope,
            "ident": ident,
        }