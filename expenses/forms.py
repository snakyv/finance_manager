from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Expense, Income, CategoryBudget


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'description', 'category', 'notes']
        widgets = {
            'description': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Опишіть витрату (наприклад: "McDonalds lunch")',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.01',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'rows': 2,
            }),
        }


class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'category', 'description']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.01',
            }),
            'category': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2',
            }),
            'description': forms.TextInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'placeholder': 'Опис доходу (зарплата, бонус тощо)',
            }),
        }


class CategoryBudgetForm(forms.ModelForm):
    class Meta:
        model = CategoryBudget
        fields = ['category', 'monthly_limit']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'w-full border rounded px-3 py-2',
            }),
            'monthly_limit': forms.NumberInput(attrs={
                'class': 'w-full border rounded px-3 py-2',
                'step': '0.01',
            }),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
