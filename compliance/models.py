from django.db import models

class Policy(models.Model):
    title = models.CharField(max_length=255)
    version = models.CharField(max_length=50)  
    description = models.TextField()
    reference_link = models.URLField(blank=True) 

class BenchmarkSection(models.Model): 
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE)
    parent_section = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True) 
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255, default='Untitled Section')
    description = models.TextField(blank=True)

class Check(models.Model):
    section = models.ForeignKey(BenchmarkSection, on_delete=models.CASCADE,  related_name='checks')
    check_number = models.CharField(max_length=10) 
    description = models.TextField()
    expected_value = models.TextField()  
    rationale = models.TextField(blank=True)
    title = models.CharField(max_length=255, default='Untitled Check')
    audit = models.TextField(blank=True)  
    remediation = models.TextField(blank=True)  
    impact = models.TextField(blank=True)  

