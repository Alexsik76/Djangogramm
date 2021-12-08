from django.contrib import admin

from auth_by_email.models import DjGrammUser, Follow
# Register your models here.

admin.site.register(Follow)

# admin.site.register(DjGrammUser)


class FollowInline(admin.TabularInline):
    model = Follow
    fk_name = "follower"


@admin.register(DjGrammUser)
class PersonAdmin(admin.ModelAdmin):
    inlines = [FollowInline]
    list_display = ('id', 'first_name', 'last_name', 'email', 'bio')


