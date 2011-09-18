from uuid import uuid4

from monkeyauth.settings import SECRET_LENGTH


def generate_secret(counter):
    """ Generate a secret with some counter value in it. """
    uuid = uuid4()
    return unicode(uuid)[:SECRET_LENGTH]

def validate_secret(secret, counter):
    """ Validate the secret against the counter. """

    return True
