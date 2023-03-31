from django.contrib.auth import forms as auth_forms
from django.contrib.admin import widgets
from django import forms
import os
import sqlite3
from .models import ImageSettings
#from .models import Image
class LoginForm(auth_forms.AuthenticationForm):
    '''ログインフォーム'''
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        for field in self.fields.values():
            field.widget.attrs['placeholder'] = field.label

class SearchForm(forms.Form):

    nameSearchField =forms.CharField(label='ゆーざーIDから状態',required=False,)
    placeSearcField =forms.IntegerField(label='出勤場所からユーザーID',required=False,)

class MakeMapForm(forms.Form):

    slicedMaps = forms.CharField(widget=forms.Textarea)
    mylist=[]
    #データベースからlistへ
    for e in ImageSettings.objects.all():
        ap=(e.pk,e.ImageName)
        mylist.append(ap)
    tup=tuple(mylist)
    #tupleに変換
    SelectMap=forms.ChoiceField(
        choices=tup,
        required=True,
        widget=forms.widgets.Select
    )
class MapNameForm(forms.Form):

    name = forms.CharField(label='部屋名',required=False,)

#index2に表示
class SelectMapForm(forms.Form):
    mylist=[]
    print(ImageSettings.objects.all())
    for e in ImageSettings.objects.all():
        ap=(e.pk,e.ImageName)
        mylist.append(ap)
    tup=tuple(mylist)
    SelectMap=forms.ChoiceField(
        choices=tup,
        required=True,
        widget=forms.widgets.Select
    )

class ImageForm(forms.ModelForm):
    class Meta:
        model = ImageSettings
        fields = ['picture', 'ImageName']
    
