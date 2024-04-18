from django import forms
from django.contrib import admin
from .models import Policy, BenchmarkSection, Check 

# Custom form for adding checks with easy Benchmark Section selection
class CheckAdminForm(forms.ModelForm):
    section = forms.ModelChoiceField(queryset=BenchmarkSection.objects.all())  

    class Meta:
        model = Check 
        fields = ('section', 'check_number', 'description', 'expected_value')

# ModelAdmin class to customize the 'Check' model in the admin
class CheckAdmin(admin.ModelAdmin):
    form = CheckAdminForm  # Use your custom form here

# Register your models with the admin interface
admin.site.register(Policy) 
admin.site.register(BenchmarkSection)
admin.site.register(Check, CheckAdmin) # Register the ModelAdmin class
