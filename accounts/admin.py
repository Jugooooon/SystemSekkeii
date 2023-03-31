# Register your models here.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import AuthUser
from django.contrib.auth.hashers import make_password
from .models import EmployeeState,ImageSettings,MapsSettings
admin.site.register(EmployeeState)
admin.site.register(ImageSettings)
admin.site.register(MapsSettings)
@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        モデルの保存

        :param request: リクエストデータ
        :param obj: ユーザモデルオブジェクト
        :param form: フォーム
        :param change: 変更フラグ
        :return: なし
        """
        if change:
            user = AuthUser.objects.get(pk=obj.pk)
            if not user.password == obj.password:
                obj.password = make_password(obj.password)
        else:
            obj.password = make_password(obj.password)
        obj.save()

    list_display = ['userID', 'last_name', 'first_name', 'email']
    ordering = ['userID']