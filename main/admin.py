from django.contrib import admin
from .models import FileEntry

@admin.register(FileEntry)
class FileEntryAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'description', 'upload_date', 'user')
    list_filter = ('upload_date',)
    search_fields = ('file_name', 'description',)
    readonly_fields = ('upload_date', 'user')
