from six import text_type
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class token(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user) + text_type(timestamp) +
            text_type(user)
        )
gentrate_token = token()

