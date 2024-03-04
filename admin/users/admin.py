from django.contrib import admin
from users.models.refresh_token import RefreshToken
from users.models.role import Role
from users.models.user import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'email', 'first_name', 'last_name',
                    'is_superuser', 'role', 'is_verified', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('is_superuser', 'role', 'is_verified')
    ordering = ('-created_at',)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'role', 'resource', 'verb')
    search_fields = ('role', 'resource', 'verb')


@admin.register(RefreshToken)
class RefreshTokenAdmin(admin.ModelAdmin):
    list_display = ('uuid', 'user', 'active_till', 'created_at', 'user_device_type')
    search_fields = ('uuid', 'user__email', 'user_device_type')
    list_filter = ('user_device_type',)
