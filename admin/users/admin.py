from django.contrib import admin

from users.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'email', 'first_name', 'last_name',
                    'is_superuser', 'role', 'is_verified', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_superuser', 'role', 'is_verified')
    ordering = ('-created_at',)

