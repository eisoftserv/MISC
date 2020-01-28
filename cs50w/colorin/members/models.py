from django.db import models
        
class MemberStatus(models.IntegerChoices):
    PRIVATE = 1
    PUBLIC = 2
    ARCHIVED = 3

class ThemeStatus(models.IntegerChoices):
    PRIVATE = 1
    PUBLIC = 2
    ARCHIVED = 3

class PlatformStatus(models.IntegerChoices):
    PRIVATE = 1
    PUBLIC = 2
    ARCHIVED = 3

class NetworkStatus(models.IntegerChoices):
    PRIVATE = 1
    PUBLIC = 2
    ARCHIVED = 3

class SuggestionStatus(models.IntegerChoices):
    PUBLIC = 1
    HIDDEN = 2
    ARCHIVED = 3

class CommentStatus(models.IntegerChoices):
    PUBLIC = 1
    HIDDEN = 2
    ARCHIVED = 3

class MessageStatus(models.IntegerChoices):
    PRIVATE = 1
    HIDDEN = 2
    ARCHIVED = 3

class FlagStatus(models.IntegerChoices):
    INITIATED = 1
    PROCESSED = 2
    ARCHIVED = 3

class ItemType(models.IntegerChoices):
    SUGGESTION = 1
    COMMENT = 2
    MESSAGE = 3
    PROFILE = 4
    REPORT = 5


class Member(models.Model):
    djuser = models.CharField(max_length=50, db_index=True)
    djemail = models.EmailField(max_length=50, db_index=True)
    status = models.IntegerField(choices=MemberStatus.choices, default=1)
    name = models.CharField(max_length=80, db_index=True)
    location = models.CharField(max_length=80, default="")
    stamp = models.CharField(max_length=30) 
    social = models.URLField(max_length=160, default="", blank=True)
    about = models.CharField(max_length=240, default="", blank=True)

    def __str__(self):
        return (f"{self.djuser} {self.name} {self.status}")
        

class Theme(models.Model):
    name = models.CharField(max_length=80, db_index=True)
    stamp = models.CharField(max_length=30)
    status = models.IntegerField(choices=ThemeStatus.choices, default=1)
   
    def __str__(self):
        return (f"{self.name} {self.status}")
        

class Platform(models.Model):       
    url = models.URLField(max_length=80, db_index=True, default="")
    stamp = models.CharField(max_length=30)
    status = models.IntegerField(choices=PlatformStatus.choices, default=1)
   
    def __str__(self):
        return (f"{self.url} {self.status}")
        

class Network(models.Model):       
    url = models.URLField(max_length=80, db_index=True, default="")
    stamp = models.CharField(max_length=30)
    status = models.IntegerField(choices=NetworkStatus.choices, default=1)
   
    def __str__(self):
        return (f"{self.url} {self.status}")


class Suggestion(models.Model):
    text = models.CharField(max_length=240)
    url = models.URLField(max_length=240, default="", blank=True)
    stamp = models.CharField(max_length=30)
    sender = models.ForeignKey(Member, on_delete=models.PROTECT, db_index=True, related_name="member_suggestions", default="")
    subject = models.ForeignKey(Theme, on_delete=models.PROTECT, db_index=True, related_name="theme_suggestions")
    author = models.CharField(max_length=160, default="", blank=True)
    title = models.CharField(max_length=80, default="")
    published = models.CharField(max_length=10, default="", blank=True)
    domain = models.ForeignKey(Platform, on_delete=models.PROTECT, db_index=True, default="", related_name="platform_suggestions")
    status = models.IntegerField(choices=SuggestionStatus.choices, default=1)

    def __str__(self):
        return (f"{self.sender.name} {self.subject.name} {self.text}")


class Comment(models.Model):
    text = models.CharField(max_length=240)
    stamp = models.CharField(max_length=30)
    sender = models.ForeignKey(Member, on_delete=models.PROTECT, db_index=True, related_name="member_comments")
    proposal = models.ForeignKey(Suggestion, on_delete=models.PROTECT, db_index=True, related_name="suggestion_comments")
    status = models.IntegerField(choices=CommentStatus.choices, default=1)

    def __str__(self):
        return (f"{self.sender.name} {self.proposal.title} {self.text}")


class Message(models.Model):
    text = models.CharField(max_length=240)
    stamp = models.CharField(max_length=30)
    sender = models.ForeignKey(Member, on_delete=models.PROTECT, db_index=True, related_name="member_sent")
    recipient = models.ForeignKey(Member, on_delete=models.PROTECT, db_index=True, related_name="member_received")
    status = models.IntegerField(choices=MessageStatus.choices, default=1)

    def __str__(self):
        return (f"{self.sender.name} {self.recipient.name} {stamp} {self.text}")


class Flag(models.Model):
    itemid = models.IntegerField( db_index=True, default=0)
    itemtype = models.IntegerField(choices=ItemType.choices, default=1)
    text = models.CharField(max_length=240)
    stamp = models.CharField(max_length=30)
    sender = models.ForeignKey(Member, on_delete=models.PROTECT, db_index=True, related_name="member_flags")
    status = models.IntegerField(choices=FlagStatus.choices, default=1)

    def __str__(self):
        return (f"{self.itemtype} {self.sender.name} {self.text}")
