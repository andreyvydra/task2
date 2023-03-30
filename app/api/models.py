from django.db import models


# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=128, blank=False)
    description = models.CharField(max_length=256, blank=True, null=True)


class Participant(models.Model):
    name = models.CharField(max_length=128, blank=False)
    wish = models.CharField(max_length=256, blank=True, null=True)
    recipient = models.ForeignKey("Participant", on_delete=models.DO_NOTHING, null=True)


class ParticipantGroup(models.Model):
    participant = models.ForeignKey("Participant", on_delete=models.CASCADE, unique=True)
    group = models.ForeignKey("Group", on_delete=models.CASCADE)
