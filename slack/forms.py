from django import forms

from .models import SlackMember, Department

class SlackMemberForm(forms.ModelForm):

    class Meta:
        model = SlackMember
        fields = ('name', 'status','department',)

class DepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = ('name', 'branch',)