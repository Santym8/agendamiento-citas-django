from django import forms
class LoginForm(forms.Form):
    correo = forms.EmailField(
        required=True,
        label='Correo Electrónico'
    )

    contraseña = forms.CharField(
        required=True,
        widget=forms.PasswordInput(),
        label='Contraseña'
    )

