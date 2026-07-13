from django.db.models.signals import post_save
from django.dispatch import receiver
from posts.models import Like
from .models import Notification
from Account.models import Follow
from comments.models import Comment
from Notifications.models import Notification


@receiver(post_save, sender=Like)
def create_like_notification(sender, instance, created, **kwargs):
    # import pdb; pdb.set_trace()
   
    if created:
        
        if instance.user != instance.post.user:
            Notification.objects.create(
                sender=instance.user,          
                receiver=instance.post.user,   
                post=instance.post,
                notification_type="like"
            )






@receiver(post_save, sender=Comment)
def create_comment_notification(sender, instance, created, **kwargs):

    if not created:
        return

    
    if instance.parent:
        if instance.author != instance.parent.author:
            Notification.objects.create(
                sender=instance.author,
                receiver=instance.parent.author,
                post=instance.post,
                notification_type="reply"
            )

    
    else:
        if instance.author != instance.post.user:
            Notification.objects.create(
                sender=instance.author,
                receiver=instance.post.user,
                post=instance.post,
                notification_type="comment"
            )

@receiver(post_save, sender=Follow)
def create_follow_notification(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(
            sender=instance.follower,
            receiver=instance.following,
            post=None,                         
            notification_type="follow"
        )
