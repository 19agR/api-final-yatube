from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author', 'group')
    search_fields = ('text', 'author__username')
    list_filter = ('pub_date', 'group')


admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Group)
admin.site.register(Post, PostAdmin)
