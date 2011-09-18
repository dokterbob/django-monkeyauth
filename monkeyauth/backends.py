from django.contrib.auth.models import User

from monkeyauth.models import SessionToken
from monkeyauth.exceptions import NotAuthenticatedException

from uuid import uuid4


class TokenBackend(object):
    def authenticate(self, secret=None):
        if secret:
            try:
                token = SessionToken.consume_token(secret)
                return token.user

            except NotAuthenticatedException:
                pass
        else:
            # Generate a secret token and create a user for it
            user = User.objects.create_user(username=uuid4())
            token = SessionToken(user=user)
            token.save()

            return user

        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
