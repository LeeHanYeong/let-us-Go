from django.db import models


class DeleteModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class DeleteModel(models.Model):
    is_deleted = models.BooleanField(default=False)

    objects = DeleteModelManager()

    class Meta:
        abstract = True

    def perform_delete(self):
        pass

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.perform_delete()
        self.save()
