from django.contrib.auth.models import User
from TimesheetApp.models import tblAuthUser
from django.core.exceptions import PermissionDenied

def link_auth_user(strategy, details, backend, uid, user=None, *args, **kwargs):
    email = details.get("email")
    print("Pipeline hit. Email received:", email)

    if not email:
        raise PermissionDenied("No email provided.")

    # Create or get Django user
    user_obj, _ = User.objects.get_or_create(username=email)

    # Try to find matching AuthUser by email
    try:
        auth_user = tblAuthUser.objects.select_related('fk_userid').get(email_address=email)
    except tblAuthUser.DoesNotExist:
        raise PermissionDenied(f"Email {email} not authorized in AuthUser.")

    if not auth_user.fk_userid_id:
        raise PermissionDenied(f"AuthUser for {email} is not linked to a valid AppUser (missing fk_userid).")

    # Store for use in middleware/view
    strategy.session_set('auth_user_id', auth_user.id)

    return {
        'user': user_obj,
        'auth_user': auth_user,
    }
