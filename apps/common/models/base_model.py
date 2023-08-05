from django_extensions.db.models import TimeStampedModel


class BaseModel(TimeStampedModel):
    class Meta:
        abstract = True

    verbose_name: str = None
    verbose_name_plural: str = None

    def __new__(cls, *args, **kwargs):
        cls.verbose_name = cls._meta.verbose_name
        cls.verbose_name_plural = cls._meta.verbose_name_plural
        return super().__new__(cls)

    def update(self, **kwargs):
        for field_name, field_value in kwargs.items():
            setattr(self, field_name, field_value)
        self.save()
