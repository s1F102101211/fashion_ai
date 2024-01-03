from django import forms

class ChatForm(forms.Form):

    sentence = forms.CharField(label='ユーザー', widget=forms.Textarea(), required=True)

class StableForm(forms.Form):
    
    sentence = forms.CharField(label='画像生成プロンプト', widget=forms.Textarea(), required=True)
