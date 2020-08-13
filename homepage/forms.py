from django import forms


class AddRecipeForm(forms.Form):
    title = forms.CharField(max_length=50)
    "author = forms.ModelChoiceField(queryset=Author.objects.all())"
    time_required = forms.CharField(max_length=20)
    description = forms.CharField(widget=forms.Textarea)
    instructions = forms.CharField(widget=forms.Textarea)


class AddAuthorForm(forms.Form):
    name = forms.CharField(max_length=80)
    bio = forms.CharField(widget=forms.Textarea)
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=240)
    password = forms.CharField(widget=forms.PasswordInput)
