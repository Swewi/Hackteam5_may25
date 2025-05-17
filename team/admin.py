from django.contrib import admin
from .models import TeamMember

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active', 'role')
    search_fields = ('name', 'bio')
    fieldsets = (
        (None, {
            'fields': ('name', 'role', 'bio', 'display_order')
        }),
        ('Social Links', {
            'fields': ('github_url', 'linkedin_url')
        }),
        ('Media', {
            'fields': ('photo',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )