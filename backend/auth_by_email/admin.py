from django.contrib import admin

from auth_by_email.models import DjGrammUser, Following
# Register your models here.


class FollowingInline(admin.TabularInline):
    model = Following
    fk_name = 'follower_user'


class FollowAdmin(admin.ModelAdmin):
    inlines = [FollowingInline, ]


admin.site.register(DjGrammUser, FollowAdmin)
