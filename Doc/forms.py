from django import forms
from .models import ContactMessage,Task

class LogoForm(forms.Form):
    pdf_file = forms.FileField(label='Select PDF file', help_text='Only PDF files are allowed', widget=forms.FileInput(attrs={'accept': 'application/pdf'}))
    logo = forms.ImageField(label='Select logo')

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
    


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['description']