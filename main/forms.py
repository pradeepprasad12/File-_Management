
from django import forms
from .models import FileEntry
from django.core.exceptions import ValidationError

class FileEntryForm(forms.ModelForm):
    class Meta:
        model = FileEntry
        fields = ['file_name', 'description', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if not file.name.lower().endswith(('.pdf', '.docx', '.tiff')):
                raise ValidationError("File type not supported. Please upload PDF, DOCX, or TIFF files.")
        return file
