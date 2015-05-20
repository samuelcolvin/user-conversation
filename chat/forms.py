from django import forms


class StartConversation(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.HiddenInput(), initial='Fred Blog')
    email = forms.CharField(max_length=255, widget=forms.HiddenInput(), initial='testing@example.com')
    hash = forms.CharField(max_length=255, widget=forms.HiddenInput(), initial='123')

    def __int__(self, *args, **kwargs):
        super(StartConversation, self).__init__(*args, **kwargs)
