from django.contrib.sessions.backends.cached_db import SessionStore as CachedStore
from tenant_schemas.utils import schema_context, get_public_schema_name

class SessionStore(CachedStore):
    def load(self):
        with schema_context(get_public_schema_name()):
            ret = super(CachedStore, self).load()
        return ret

    def save(self, must_create=False):
        with schema_context(get_public_schema_name()):
            ret = super(CachedStore, self).save(must_create)
        return ret

    def delete(self, session_key=None):
        with schema_context(get_public_schema_name()):
            ret = super(CachedStore, self).delete(session_key)
        return ret

    def flush(self):
        with schema_context(get_public_schema_name()):
            ret = super(CachedStore, self).flush()
        return ret
