from django.contrib import admin
from django.urls import path,include 
from django.views.generic import base
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title = '管理メニュー'
admin.site.site_header = '管理メニュー'
admin.site.index_title = 'メニュー'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/',include('accounts.urls')), 
]+  static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)
