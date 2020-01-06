import uuid
from django.db import models

# Create your models here.
class Policy(models.Model):
    uid = models.UUIDField(primary_key=False, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    insured = models.UUIDField(primary_key=False)
    description = models.CharField(max_length=250)

    def serialize(self):
        return dict(
            uid=self.uid,
            name=self.name,
            insured = {"uid": self.insured},
            description=self.description
        )


