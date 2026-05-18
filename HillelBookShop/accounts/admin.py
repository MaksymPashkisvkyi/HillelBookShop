from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'full_name', 'phone', 'is_active', 'is_staff', 'date_joined')
    ordering = ('email',)
    list_display_links = ('email',)

    fieldsets = (
        (_('Basic information'), {'fields': ('email', 'password')}),
        (_('Personal information'),
         {'fields': ('first_name', 'last_name', 'phone', 'date_of_birth', 'profile_image')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            }
        ),
    )

    @admin.display(description=_('Full name'))
    def full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'.strip()
