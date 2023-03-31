# Create your views here.
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy 
from django.http import HttpResponse, request
from django.urls import reverse
from urllib.parse import urlencode
from . import forms
from . import models
from .models import EmployeeState,MapsSettings,ImageSettings
from django.template import context
import sqlite3
from django.db.models import Min
from django.contrib.auth.decorators import login_required
from .forms import SearchForm,MakeMapForm,MapNameForm,SelectMapForm
from .forms import ImageForm
from .dbManage import StateSearch,PlaceSearch,TableInfo,empStateDic,RatestMapNum,SelectMap
from .AddMap import CheckinMaps,BuildHTML
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

def index(request):
    return render(request, "accounts/index.html")


class MyLoginView(LoginView):
    form_class = forms.LoginForm
    template_name = "accounts/login.html"


class MyLogoutView(LoginRequiredMixin, LogoutView):
    template_name = "accounts/logout.html"

@login_required
def index2(request):
    f = SelectMapForm()
    username = request.user.userID
    data = EmployeeState.objects.all().filter(userID=username)
    print(ImageSettings.objects.all())
    params = {'data': data,'form':f}
    if(request.method =='POST'):
        f = SelectMapForm(request.POST)
        if(f.is_valid()):
            val=f.cleaned_data['SelectMap']
            #ここからshowmapにvalを渡す
            redirect_url = reverse('showMap')
            # パラメータのdictをurlencodeする。複数のパラメータを含めることも可能
            parameters = urlencode({'param': val})
            # # URLにパラメータを付与する
            url = f'{redirect_url}?{parameters}'
            return redirect(url)
            #return redirect("showMap")

    return render(request, "accounts/index2.html",params)
@login_required
def StateView(request):
    template_name = "accounts/state.html"

    if request.method == "POST":
        
        state = request.POST.get('state', '0')
        username = request.user.userID

        '''EmployeeState.objects.filter(userID=username).delete()
        EmployeeState.objects.update_or_create(
            userID=username,
            EMPstate=state,
        )'''

        if state == '10':
            S = EmployeeState.objects.filter(userID=username).first()
            S.EMPstate = state
            S.RoomID = 0
            S.save()

        else:
            S = EmployeeState.objects.filter(userID=username).first()
            S.EMPstate = state
            S.save()

        return redirect("index2")

    else:
        return render(request, template_name)


    return(request, template_name)

def Search(request):
    url = 'accounts/search.html'
    f = SearchForm()
    result = ['','']
    if(request.method =='POST'):
        #入力が入ってきた
        f=SearchForm(request.POST)
        #値があるなら
        if(f.is_valid()):
            res = f.cleaned_data
            result = [StateSearch(res['nameSearchField']),PlaceSearch(res['placeSearcField'])]
    return render(request,url,
                  {'form':f,'searchResult':result[0],'placeResult':result[1]})
@login_required

def MakeMaps(request):
    #マップ追加
    url = 'accounts/makeMaps.html'
    f = MakeMapForm()
    if(request.method =='POST'):
        #イメージマップジェネレータからもらってきた
        f = MakeMapForm(request.POST)
        print(f)
        cm = CheckinMaps()
        val=f.cleaned_data['SelectMap']

        slicedTexts = cm.SplitTexts(f.cleaned_data['slicedMaps'])
        cm.NumberingImagemapShapes(slicedTexts,val)
        return redirect("index2")

    else:
        return render(request,url,{'form':f})

def MakeImages(request):
    #画像追加
    if request.method == "POST":
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('index2')
    else:
        form = ImageForm()

    context = {'form':form}
    return render(request, 'accounts/addImage.html', context)

@csrf_exempt
def ShowMap(request):
    m = BuildHTML()
    #index2からのvalを取得
    val = request.GET.get('param')
    obj = ImageSettings.objects.filter(id=val).first()
    #条件を満たす画像のパス取得
    Pic1=getattr(obj, 'picture')
    #条件を満たすレコードを取得
    s = SelectMap(val)
    username = request.user.userID
    data = EmployeeState.objects.all()
    params = {'data': data}
    if request.method == "POST":
        
        room = request.POST.get('get_room_name', '0')
        username = request.user.userID

        S = EmployeeState.objects.filter(userID=username).first()
        S.RoomID = room
        S.save()
        
        return redirect("index2")
    else:
        return HttpResponse(m.Build('/'+str(Pic1),m.MakeMap(s)))

class RoomsView(ListView, LoginRequiredMixin):
    model = EmployeeState

    def get_queryset(self):

        if 'name' in self.request.GET:
            q_word = self.request.GET.get('name')
            object_list = EmployeeState.objects.filter( Q(userID__icontains=q_word) ) 

        elif 'state' in self.request.GET:
            q_word = self.request.GET.get('state')
            object_list = EmployeeState.objects.filter( Q(EMPstate__iexact=q_word) )

        elif 'room' in self.request.GET:
            q_word = self.request.GET.get('room')
            object_list = EmployeeState.objects.filter( Q(RoomID__iexact=q_word) )

        else:
            object_list = EmployeeState.objects.all()
        return object_list
def test(request):
    return render(request, 'accounts/test.html')

def CheckIn(request):
    #部屋の場所変更
    template_name = "accounts/shirahama1f.html"
    username = request.user.userID
    data = EmployeeState.objects.all()
    params = {'data': data}

    if request.method == "POST":
        
        room = request.POST.get('get_room_name', '0')
        username = request.user.userID

        S = EmployeeState.objects.filter(userID=username).first()
        S.RoomID = room
        S.save()

        return redirect("index2")

    else:
        return render(request, template_name, params)


    return(request, template_name, params)

def CheckIn2(request):
    #部屋の場所変更
    template_name = "accounts/shirahama2f.html"
    username = request.user.userID
    data = EmployeeState.objects.all()
    params = {'data': data}

    if request.method == "POST":
        
        room = request.POST.get('get_room_name', '0')
        username = request.user.userID

        S = EmployeeState.objects.filter(userID=username).first()
        S.RoomID = room
        S.save()
        
        return redirect("index2")

    else:
        return render(request, template_name, params)


    return(request, template_name, params)

