from django.contrib import admin

from products.admin import BasketAdmin
from users.models import EmailVerification, User


class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)
    inlines = (BasketAdmin,)


class EmailVerificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'expiration', 'code',)
    fields = ('user', 'expiration', 'created_at', 'code',)
    readonly_fields = ('created_at', 'code',)


admin.site.register(User, UserAdmin)
admin.site.register(EmailVerification, EmailVerificationAdmin)

