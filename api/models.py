from django.db import models


# Create Messages Model
class Message(models.Model):
    title = models.CharField(max_length=100)
    body = models.TextField()
    read = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    author = models.ForeignKey('auth.User', related_name='messages', on_delete=models.CASCADE)

    def mark_read(self):
        self.read = True

    def sending(self):
        self.send = True
