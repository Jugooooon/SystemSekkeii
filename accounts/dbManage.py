
import sys
sys.path.append('..')

import sqlite3
from django.contrib import admin
from myproject.settings import DATABASES
from .models import MapsSettings

#select name from sqlite_master where type='table';
tableNames = [('django_migrations',), ('sqlite_sequence',), ('django_content_type',), ('auth_group_permissions',), ('auth_permission',),
             ('auth_group',), ('accounts_employeestate',), ('accounts_authuser',), ('accounts_authuser_groups',), ('accounts_authuser_user_permissions',),
            ('accounts_mapssettings',), ('django_admin_log',), ('django_session',)]

empStateDic = {0:'入力なし',1:'出勤',2:'社用外出',3:'私用外出',4:'遅刻',5:'早退',6:'休み',7:'午前休',8:'午後休',9:'テレワーク',10:'退社',11:'出張'}    

#データベースに接続しexeCodeを実行
def Execute(exeCode):
    dbPath = DATABASES['default']['NAME']
    connection = sqlite3.connect(dbPath)
    cursor = connection.cursor()
    cursor.execute(exeCode)
    result = cursor.fetchall()
    cursor.close()
    print(exeCode)
    return result
#ユーザーIDでaccounts_employeestateのEMPstateを取得
def StateSearch(name):
 
    state ='ユーザーIDが存在しませんでした'
    if name!=None:
        exeCode = 'select *from '+tableNames[6][0]+' where userID = '+"'"+name+"'"
        result = Execute(exeCode)
        if result!=[]:

            state = result[0][3]
    return state
#ユーザーIDで部屋の場所を検索
def PlaceSearch(placeNum):
  
    places ='指定した場所に出勤した人はいませんでした'
    if placeNum!=None:
        exeCode = 'select userID from '+tableNames[6][0]+' where RoomID = '+str(placeNum)
        print(exeCode)
        result = Execute(exeCode)
        if result!=[]:

            places = result
    return places
#フィールド名取得    
def TableInfo(num):

    exeCode = 'PRAGMA table_info('+tableNames[num][0]+')'
    return Execute(exeCode)
#マップ情報の追加
def AddMap(name,shape,coords,Image):
    m = MapsSettings(RoomName=name,Shape=shape,Coords=coords,Image_id=Image)
    m.save()
#マップ情報をstartからendまで取得
def SelectMap(imageID):

    cmd = 'select *from '+tableNames[10][0]+' where Image_id ='+str(imageID)
    return Execute(cmd)
#一番新しいマップ番号
def RatestMapNum():

    exeCode = 'select max(id) from '+tableNames[10][0]
    return Execute(exeCode)
#テーブル名取得
def TableNames():

    exeCode = "select name from sqlite_master where type='table'"
    tableNames = Execute(exeCode)

TableNames()
