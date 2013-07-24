from django.contrib.auth import get_user_model


class ModelEmailBackend(object):
    """
    Authenticates against account.User
    """
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            UserModel = get_user_model()
            return UserModel._default_manager.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None