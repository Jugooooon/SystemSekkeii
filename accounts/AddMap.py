from .dbManage import AddMap,RatestMapNum
from re import findall
import sys

class CheckinMaps(object):
    #
    def __init__(self,):
        #edge を環境に合わせないと
        self.edge = r'C:\Users\BOUfU\Documents\System_Planing\System_Planning\edgedriver_win64\msedgedriver.exe'
        self.url = 'https://labs.d-s-b.jp/ImagemapGenerator/'
        self.cssSelector = 'body > div > div.row.playground > div.col-sm-4.code.ex-code-prettify-hide-demo > div.ex-code-prettify-contents > pre > ol'
    #文字列分け
    def SplitTexts(self,texts):

        slicedText = texts.split('\r\n')
        return slicedText[1:-1]
    #番号付け
    def NumberingImagemapShapes(self,texts,val):

        # <area shape="rect" coords="202,328,534,636" href="#" alt="" />
        start = RatestMapNum()
        if(start[0][0]==None):

            start=0
        else:
            
            start = start[0][0]
        result=[]
        for i in range(len(texts)):
            num = i+start
            text = texts[i]
            #番号付け
            text = text.replace('alt=""','alt='+str(num))
            #分追加
            text = text.replace('/>','onclick="getname(this.alt)"/>')
            result.append(text)
            #切り分けた形を抽出
            #切り分けたマップを抽出
            shape = findall(r'shape="(.+)" coords=',text)[0]
            coords = findall(r'coords="(.+)" href=',text)[0]
            #DBに登録　とりあえず名前は'test{num}'
            AddMap('test'+str(num),shape,coords,val)
        
        return result
    #html組み立te
    

class BuildHTML(object):

    def __init__(self):
        pass

    def MakeMap(self,mapDatas):

        areas = []
        for m in mapDatas:
            a = '<area shape="'+m[2]+'"'+'coords="'+m[3]+'" nohref alt ='+str(m[0])+' onclick="'+'getname(this.alt)"/>'
            areas.append(a)
        return areas

    def Build(self,imgURL,areas):

        head = '<head><meta charset="utf-8" /><title></title></head>'
        homeLink = ' <a href="{% url '+'index2'+' %}">戻る</a><br> '
        inputForm ='<tr><td align="right"><b> 入力した場所：</b></td><td><input type="text" name="get_room_name" size="30" maxlength="10" value="0" required> <input type="submit" name="statebuttom"></td></tr>'
        loadStatic = "{% load static %}{% csrf_token %}"
        print(loadStatic)
        img = '<img src="'+imgURL+'" usemap="#ImageMap" alt="" />'
        maps='<map name="ImageMap">'
        for area in areas:

            maps=maps+area
        script = '<script>function getname(alt){document.room.get_room_name.value =alt;}</script>'
        maps=maps+script
        maps=maps+'</map>'

        forms = '<form name="room" id="room" method="POST">'+inputForm+img+maps+'</form>'
        result = '<html>'+head+'<body>'+forms+'<body>'+'<html>'
        return result

    def Build_test(self,imgURL,areas):
        '''
        {% csrf_token %}
        '''
        img = '<img src="'+imgURL+'" alt="" >'
        temp ='<!DOCTYPE><html><head><title>title</title>'+img+'</head><html>'

        return temp
        



