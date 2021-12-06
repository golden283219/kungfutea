import uuid
from django.db import models

class SopAndPosLink(models.Model):
    SOP_link = models.CharField(max_length=1024)
    POS_link = models.CharField(max_length=1024)
    def __str__(self):
        return self.SOP_link