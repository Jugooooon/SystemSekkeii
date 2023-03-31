from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models import CASCADE
from django.utils import timezone

# Create your models here.



class AuthUserManager(BaseUserManager):
    def create_user(self, userID, email, password, last_name, first_name):
        """
        ユーザ作成

        :param userID: ユーザID
        :param email: メールアドレス
        :param password: パスワード
        :param last_name: 苗字
        :param first_name: 名前
        :return: AuthUserオブジェクト
        """
        if not email:
            raise ValueError('Users must have an email') 
        if not userID:
            raise ValueError('Users must have an userID')

        user = self.model(userID=userID,
                          email=email,
                          password=password,
                          last_name=last_name,
                          first_name=first_name)

        user.is_active = True
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, userID, email, password, last_name, first_name):
        """
        スーパーユーザ作成

        :param userID: ユーザID
        :param email: メールアドレス
        :param password: パスワード
        :param last_name: 苗字
        :param first_name: 名前
        :return: AuthUserオブジェクト
        """
        user = self.create_user(userID=userID,
                                email=email,
                                password=password,
                                last_name=last_name,
                                first_name=first_name)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class AuthUser(AbstractBaseUser, PermissionsMixin):
    """
    ユーザ情報を管理する
    """
    class Meta:
        verbose_name = 'ユーザ'
        verbose_name_plural = 'ユーザ'

    def get_short_name(self):
        """
        ユーザの苗字を取得する

        :return: 苗字
        """
        return self.last_name

    def get_full_name(self):
        """
        ユーザのフルネームを取得する

        :return: 苗字 + 名前
        """
        return self.last_name + self.first_name

    userID = models.CharField(verbose_name='ユーザID',
                                unique=True,
                                max_length=30)
    last_name = models.CharField(verbose_name='苗字',
                                 max_length=30,
                                 default=None)
    first_name = models.CharField(verbose_name='名前',
                                  max_length=30,
                                  default=None)
    email = models.EmailField(verbose_name='メールアドレス',
                              null=True,
                              default=None)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(verbose_name='有効フラグ',
                                    default=True)
    is_staff = models.BooleanField(verbose_name='管理サイトアクセス権限',
                                   default=False)

    USERNAME_FIELD = 'userID'
    REQUIRED_FIELDS = ['email', 'last_name', 'first_name']
    objects = AuthUserManager()

    def __str__(self):
        return self.last_name + ' ' + self.first_name
#state表  0:出勤  1:社用外出  2:私用外出  3:遅刻  4:早退  5:休み  6:午前休  7:午後休  8:テレワーク  9:退社  10:出張
class EmployeeState(models.Model):
    #userID = models.ForeignKey(AuthUser, on_delete=CASCADE, null=True, blank=True)
    userID = models.CharField(max_length=100, null=False, blank=True, primary_key=True)
    EMPstate = models.CharField(max_length=100, null=True, blank=True)
    RoomID = models.CharField(max_length=100, null=True, blank=True)
    regist_date = models.DateTimeField(default=timezone.now)

class ImageSettings(models.Model):
    picture = models.ImageField(upload_to='static/pics/',null=True)
    ImageName = models.CharField(max_length=100)
    def __str__(self):
        return self.ImageName

class MapsSettings(models.Model):
    RoomName = models.CharField(max_length=100)
    Shape = models.CharField(max_length=100)
    Coords = models.CharField(max_length=100)
    Image = models.ForeignKey(ImageSettings, null=True,on_delete=models.CASCADE)
