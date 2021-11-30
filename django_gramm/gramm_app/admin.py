from django.contrib import admin
from gramm_app.models import Post
# Register your models here.


# @admin.register(DjGrammUser)
# class PersonAdmin(admin.ModelAdmin):
#     list_display = ('id', 'first_name', 'last_name', 'email', 'bio')


admin.site.register(Post)
