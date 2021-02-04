from rest_framework.throttling import SimpleRateThrottle


class VisitThrottle(SimpleRateThrottle):
    """
    对游客节流限制
    """
    scope = 'Vistor'

    def get_cache_key(self, request, view):
        # 唯一表示是IP
        return self.get_ident(request)


class UserThrottle(SimpleRateThrottle):
    """
    对登陆用户节流限制
    """
    scope = 'User'

    def get_cache_key(self, request, view):
        # 唯一表示是用户名
        return request.user
