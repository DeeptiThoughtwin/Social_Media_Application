from apps.posts.model import Post
from django.core.cache import cache
from django.db.models.signals import post_save,post_delete
from django.dispatch import receive

@receiver(post_save, sender=Post)
def clear_posts_cache_on_save(sender, **kwargs):
    cache.delete("home_posts")


@receiver(post_delete, sender=Post)
def clear_posts_cache_on_delete(sender, **kwargs):
    cache.delete("home_posts")