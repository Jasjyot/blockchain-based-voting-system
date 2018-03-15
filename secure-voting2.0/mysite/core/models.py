from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class PollBlockchain(models.Model):

    receiverId = models.CharField(max_length=120)
    timeStampVote = models.CharField(max_length=64)
    #[Sun Nov 15 02:18:12 2009]

    prevHash = models.CharField(max_length=64)
    blockHash = models.CharField(max_length=64)
    nonce = models.CharField(max_length=64)

    def __str__(self):
        return self.receiverId

    def __str__(self):
        return self.timeStampVote

    def __str__(self):
        return self.prevHash

    def __str__(self):
        return self.blockHash

    def __str__(self):
        return self.nonce

class UserProfile(models.Model):
    user = models.CharField(max_length=120)
    #email = models.CharField(max_length=60)
    isVoteCasted = models.BooleanField(default=False)

    def __str__(self):
        return self.user

    def __bool__(self):
        return self.isVoteCasted

