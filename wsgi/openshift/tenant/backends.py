from django.contrib.auth.backends import ModelBackend
from tenant_schemas.utils import schema_context, get_public_schema_name

class MasterUserBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        with schema_context(get_public_schema_name()):
            ret = super(MasterUserBackend, self).authenticate(username, password)
        return ret

    def get_user(self, user_id):
        with schema_context(get_public_schema_name()):
            ret = super(MasterUserBackend, self).get_user(user_id)
        return ret
