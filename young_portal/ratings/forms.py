from django import forms
from .models import DocumentSubmission

class DocumentSubmissionForm(forms.ModelForm):
    class Meta:
        model = DocumentSubmission
        fields = ['document_type', 'file_path']
        widgets = {
            'document_type': forms.Select(attrs={'class': 'form-select'}),
        }
