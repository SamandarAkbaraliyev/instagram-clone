from django.db.models import Model, DateTimeField


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    modified_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True
