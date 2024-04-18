import winreg
from django.shortcuts import render
from rest_framework import viewsets, serializers
from .serializers import PolicySerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .compliance_helpers import check_password_history, check_password_complexity, check_maximum_password_age
from .check_helpers import check_guest_account_status
from rest_framework import serializers
from .models import Policy, BenchmarkSection, Check


class PolicyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer

class ComplianceCheckView(APIView):
    def post(self, request):
        policy_id = request.data.get('policy_id')

        try:
            policy = Policy.objects.get(pk=policy_id)
        except Policy.DoesNotExist:
            return Response({'error': 'Policy not found'}, status=404)

        compliance_report = self.generate_compliance_report(policy) 
        return Response(compliance_report)
    

    def generate_compliance_report(self, policy):
        compliance_report = {}

        for section in policy.benchmarksection_set.all():  # Use the related name
            section_result = {'section_title': section.title, 'checks': []}

            for check in section.checks.all():
                check_result = self.perform_compliance_check(check)
                check_result['actual_value'] = self.get_actual_value(check) 
                section_result['checks'].append(check_result)

            compliance_report[section.title] = section_result 
        return compliance_report


    def perform_compliance_check(self, check):
        status = 'FAIL'  

        if check.description == 'Enforce Password Complexity':
            status = check_password_complexity()  
        elif check.description == 'Disable Guest Account':
            status = check_guest_account_status() 
        elif check.description == 'Enforce Password History':
            expected_history_size = check.expected_value
            status = check_password_history(expected_history_size)
        elif check.description == 'Ensure Maximum Password Age':  
            expected_max_age = check.expected_value 
            status = check_maximum_password_age(expected_max_age) 

        return {
            'check_title': check.title,
            'status': status,
            'expected_value': check.expected_value,  
        }
    
    def get_actual_value(self, check):
        if check.description == 'Disable Guest Account':
            return 'ENABLED' if check_guest_account_status() == 'FAIL' else 'DISABLED'
        elif check.description == 'Enforce Password History':
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
                actual_history_size, _ = winreg.QueryValueEx(key, "PasswordHistorySize") 
                return str(actual_history_size)
            except FileNotFoundError:
                return 'NOT FOUND'
    
        elif check.description == 'Ensure Maximum Password Age': 
            try:
                key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System")
                actual_max_age, _ = winreg.QueryValueEx(key, "MaximumPasswordAge") 
                return str(actual_max_age // 86400)  # Convert to days
            except FileNotFoundError:
                return 'NOT FOUND'
        
        else:
            return 'NOT IMPLEMENTED' 
    

class CheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Check
        fields = '__all__'

class BenchmarkSectionSerializer(serializers.ModelSerializer):
    checks = CheckSerializer(many=True, read_only=True) 
    class Meta:
        model = BenchmarkSection
        fields = '__all__'

class PolicySerializer(serializers.ModelSerializer):
    sections = BenchmarkSectionSerializer(many=True, read_only=True)
    class Meta:
        model = Policy
        fields = '__all__' 

