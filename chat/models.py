from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)


class Conversation(models.Model):
    customer = models.ForeignKey(Customer)

    def __str__(self):
        return u'Conversation with %s' % self.customer.email


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    timestamp = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, null=True)
    text = models.TextField()
