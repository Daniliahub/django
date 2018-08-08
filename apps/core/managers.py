from django.db import models


class BaseManager(models.Manager):
    """
    Core Manager to manage queries
    """
    def delete(self, *args, **kwargs):
        """
        Do not delete anything from database, just set trashed True
        """
        return super(BaseManager, self).get_queryset().update(trashed=True)

    def get_or_none(self, **kwargs):
        data = super(BaseManager, self).filter(**kwargs)
        if not data:
            data = None
        return data[0]

    def get_queryset(self):
        """
        Override get_queryset to not show deleted objects, so normal filter queries won't show hidden
        or trashed objects
        """
        return super(BaseManager, self).get_queryset().filter(trashed=False, hidden=False)

    def default_filter(self, *args, **kwargs):
        """
        Sometimes you want to see all (trashed, hidden, not trashed, not hidden) objects
        """
        return super(BaseManager, self).get_queryset().filter(*args, **kwargs)

