from django import forms

from .models import SignUp,Document,Friends,Request_send,Friends,Shared,Details,PrivacyDetails,PrivacyFriend,PrivacyDocs


class ContactForm(forms.Form):
    full_name = forms.CharField()
    email = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

class SignUpForm(forms.ModelForm):
    class Meta:
        model = SignUp
        fields = ['full_name', 'email']

#class UploadFileForm(forms.Form):
        #title = forms.CharField(max_length=50)
        #file = forms.FileField()

class DocumentForm(forms.ModelForm):
    #title = forms.CharField(max_length=50)
    #print title
    #docfile = forms.FileField()
    class Meta:
        model=Document
        fields = ['docfile']
class FriendForm(forms.ModelForm):
    class Meta:
        model= Friends
        exclude = ['user_name','friend_name']
class RequestSendForm(forms.ModelForm):
    class Meta:
        model=Request_send
        exclude= ['user_name','friend_req','document_name']

class SharedForm(forms.ModelForm):
    class Meta:
        model = Document
        exclude= ['user_name','docfile','read','write','owner']


class SaveForm(forms.Form):
    filePath = forms.CharField(widget = forms.HiddenInput(),max_length=100,required=False)
    message= forms.CharField(widget=forms.Textarea,label='',required=False)

class SaveDetailsForm(forms.ModelForm):
    class Meta:
        model = Details
        exclude = ['user_name','name','age','location','phnumber','email']

class PrivacyDetailsForm(forms.ModelForm):
    class Meta:
        model = PrivacyDetails
        exclude = ['user_name','name','age','location','phnumber','email']

class PrivacyFriendForm(forms.ModelForm):
    class Meta:
        model = PrivacyFriend
        exclude = ['user_name','privacy']
class PrivacyDocumentForm(forms.ModelForm):
    class Meta:
        model = PrivacyDocs
        exclude = ['user_name','docfile','privacy']
#class RequestRecvForm(forms.ModelForm):
    #class Meta:
        #model=Request_recv
        #exclude= ['user_name','friend_req']