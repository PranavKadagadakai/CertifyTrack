from django.contrib import admin
from .models import Club, Profile, CertificateTemplate, Event, Certificate

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'admin', 'created_at')
    search_fields = ('name', 'admin__username')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'phone')  # Ensure these fields exist in Profile

if not admin.site.is_registered(Profile):
    admin.site.register(Profile, ProfileAdmin)
    

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'club', 'status', 'date', 'created_at')
    search_fields = ('name', 'club__name')

@admin.register(CertificateTemplate)
class CertificateTemplateAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'uploaded_at')
    search_fields = ('event__name',)

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('id', 'generated_at')  # Adjust fields as needed

if not admin.site.is_registered(Certificate):
    admin.site.register(Certificate, CertificateAdmin)