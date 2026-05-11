from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_redis import get_redis_connection

class Tier(models.Model):
    name = models.CharField(max_length=50, unique=True)
    max_requests_reference = models.IntegerField(default=100) 

    def __str__(self):
        return self.name

class UserRateLimitProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rate_limit_profile')
    tier = models.ForeignKey(Tier, on_delete=models.PROTECT)
    cycle = models.CharField(max_length=50, default='2025_01') 

    def __str__(self):
        return f"{self.user.username} | {self.tier.name}"

@receiver(post_save, sender=UserRateLimitProfile)
def sync_to_redis(sender, instance, **kwargs):
    try:
        con = get_redis_connection("default")
        redis_key = f"user_meta:{instance.user.id}"
        
        con.hset(redis_key, mapping={
            "tier": instance.tier.name,
            "cycle": instance.cycle
        })
    except Exception as e:
        print(f"Redis Error: {str(e)}")