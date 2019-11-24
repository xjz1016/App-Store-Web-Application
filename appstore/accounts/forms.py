from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from accounts.models import User
from app.models import Developer, Reviewer

class ReviewerSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_reviewer = True
        user.save()
        reviewer = Reviewer.objects.create(reviewer=user)
        return user


class DeveloperSignUpForm(UserCreationForm):
    developer_name = forms.CharField(max_length=50)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_developer = True
        user.save()
        developer = Developer.objects.create(developer_account=user)
        developer.developer_name = self.cleaned_data.get('developer_name')
        return user


