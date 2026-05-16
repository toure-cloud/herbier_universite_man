from django.contrib import admin
from .models import SuperAdmin, OTPCode, APICache, APISyncLog

@admin.register(SuperAdmin)
class SuperAdminAdmin(admin.ModelAdmin):
    list_display = ('email', 'nom', 'telephone', 'pays_code', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'is_superuser')
    search_fields = ('email', 'nom', 'telephone')
    readonly_fields = ('date_joined', 'last_login')
    fieldsets = (
        ('Informations personnelles', {
            'fields': ('email', 'nom', 'telephone', 'pays_code')
        }),
        ('Authentification', {
            'fields': ('password', 'is_active', 'is_staff', 'is_superuser')
        }),
        ('Dates', {
            'fields': ('date_joined', 'last_login')
        }),
    )

@admin.register(OTPCode)
class OTPCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'type', 'created_at', 'expires_at', 'is_used')
    list_filter = ('type', 'is_used')
    search_fields = ('user__email', 'code')
    readonly_fields = ('created_at',)

@admin.register(APICache)
class APICacheAdmin(admin.ModelAdmin):
    list_display = ('endpoint', 'last_update')
    search_fields = ('endpoint',)

@admin.register(APISyncLog)
class APISyncLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('action', 'message')
    readonly_fields = ('created_at',)
