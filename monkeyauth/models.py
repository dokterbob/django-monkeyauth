from django.db import models
from django.contrib.auth.models import User

from monkeyauth.settings import SECRET_LENGTH
from monkeyauth.exceptions import NotAuthenticatedException
from monkeyauth.utils import generate_secret, validate_secret


class SessionToken(models.Model):
    user = models.ForeignKey(User)
    counter = models.IntegerField(default=0)
    secret = models.CharField(default=generate_secret,
                              max_length=SECRET_LENGTH, primary_key=True)

    def verify(self):
        return validate_secret(self.secret, self.counter)

    def update(self):
        """ Invalidate the old token, generate a new one. """
        self.counter += 1
        self.secret = generate_secret()

        # Note: this *might* raise a validationerror when the secret is not
        # unique
        self.save()

        return self


    @classmethod
    def _get_token(self, token_str):
        try:
            return self.objects.get(secret=token_str)
        except SessionToken.DoesNotExist:
            return None

    @classmethod
    def consume_token(self, token_str):
        token = self._get_token(token_str)

        if token and token.verify():
            return token.update()
        else:
            raise NotAuthenticatedException()


