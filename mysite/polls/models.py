from django.db import models

class AudioFile(models.Model):
    file = models.FileField(upload_to='audio/')

    class Meta:
        app_label = 'polls'