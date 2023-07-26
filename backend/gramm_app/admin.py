from django.contrib import admin
from gramm_app.models import Post, Like
# Register your models here.


class LikeInline(admin.TabularInline):
    model = Like
    fk_name = 'liked'


class LikeAdmin(admin.ModelAdmin):
    inlines = [LikeInline, ]


admin.site.register(Post, LikeAdmin)
