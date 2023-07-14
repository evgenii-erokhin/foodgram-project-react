from django.contrib import admin

from users.models import User, Follow


class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    search_fields = ('first_name',)
    list_filter = ('email', 'first_name')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')


admin.site.register(User, UserAdmin)
admin.site.register(Follow, FollowAdmin)
