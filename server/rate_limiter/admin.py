from django.contrib import admin
from .models import Tier, UserRateLimitProfile

@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    list_display = ('name', 'max_requests_reference')

@admin.register(UserRateLimitProfile)
class UserRateLimitProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'tier', 'cycle')
    search_fields = ('user__username', 'user__email')
    list_filter = ('tier',)
    raw_id_fields = ('user',)

    