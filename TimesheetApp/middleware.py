from TimesheetApp.models import tblAuthUser

class ForceGoogleAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.auth_user = None

        if request.user.is_authenticated:
            try:
                request.auth_user = tblAuthUser.objects.select_related('fk_userid__fk_roleid').get(email_address=request.user.username)
                # request.auth_user = tblAuthUser.objects.select_related('fk_userid').get(email_address=request.user.username)

            except tblAuthUser.DoesNotExist:
                request.auth_user = None

        return self.get_response(request)

