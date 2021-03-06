#coding=utf-8
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.core import serializers

from tea.models import Cloth, ClothImg, ClothSize, ClothDesc, Order, ClothUpload
from tea.forms import RegisterForm, OrderForm, ClothUploadForm

from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):

    return render(request, 'tea/index.html', None)


def get_cloth(request, cloth_id):

    cloth_id = int(cloth_id)

    cloth = []
    cloth.append(Cloth.objects.get(pk=cloth_id))
    data = serializers.serialize('json', cloth)
    return HttpResponse(data)


def get_cloth_list(request, start_id, limit):

    # start_id -= 1 # for hyz
    start_id = int(start_id) - 1
    limit = int(limit)

    cloth_list = Cloth.objects.filter(online=True)[start_id:start_id+limit]
    data = serializers.serialize('json', cloth_list)
    return HttpResponse(data)


def get_cloth_imgs(request, cloth_id):

    cloth_id = int(cloth_id)

    cloth_imgs = ClothImg.objects.filter(cloth=cloth_id)
    data = serializers.serialize('json', cloth_imgs)
    return HttpResponse(data)



def get_cloth_desc(request, cloth_id):

    cloth_id = int(cloth_id)

    cloth_desc = ClothDesc.objects.filter(cloth=cloth_id)
    data = serializers.serialize('json', cloth_desc)
    return HttpResponse(data)



def get_cloth_sizes(request, cloth_id):

    cloth_id = int(cloth_id)

    cloth_sizes = ClothSize.objects.filter(cloth=cloth_id)
    data = serializers.serialize('json', cloth_sizes)
    return HttpResponse(data)


# user
#--------------------------------------------------------------------

def user_info(request):

    if not request.user.is_authenticated():
        return HttpResponse("None")

    user = request.user
    data = serializers.serialize('json', (user,))
    return HttpResponse(data)


def login_view(request):

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponse('ok')
        return HttpResponse('None')
    else:
        return render(request, 'tea/login.html', None)

def logout_view(request):

    logout(request)
    return HttpResponse('ok')

def register(request):

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']

            user = User.objects.create_user(username, password=password, email=email)
            if user is not None:
                user.save()
                return HttpResponse('ok')
        return HttpResponse('None')
    else:
        form = RegisterForm()
        form_dict = {
            'form': form,
        }
        return render(request, 'tea/register_form.html', form_dict)


# ----------------------------------------
@login_required
def make_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            user_id = form.cleaned_data['user_id']
            user = User.objects.get(pk=user_id)
            cloth_id = form.cleaned_data['cloth_id']
            cloth = Cloth.objects.get(pk=cloth_id)
            num = form.cleaned_data['num']
            price = cloth.price

            order = Order(user=user, cloth=cloth, num=num, sum_price=num*price)
            order.save()
            return HttpResponse('ok')
        return HttpResponse('None')
    else:
        form = OrderForm()
        form_dict = {
            'form': form,
        }
        return render(request, 'tea/order_form.html', form_dict)

@login_required
def user_orders(request):

    user = request.user
    orders = user.order_set.all()
    data = serializers.serialize('json', orders)
    return HttpResponse(data)



# cloth display
#---------------------------------------------------------------------------------
def cloth_list(request):

    cloth_list = Cloth.objects.all()
    cloth_dict = {
        'title': '衣服列表',
        'cloth_list': cloth_list,
    }
    return render(request, 'tea/cloth_list.html', cloth_dict)

def cloth_detail(request, cloth_id):

    cloth = Cloth.objects.get(pk=cloth_id)
    cloth_dict = {
        'title': '衣服详细',
        'cloth': cloth,
    }
    return render(request, 'tea/cloth_detail.html', cloth_dict)



def cloth_show(request, cloth_id):

    cloth = Cloth.objects.get(pk=cloth_id)
    cloth_dict = {
        'title': '衣服详细',
        'cloth': cloth,
    }
    return render(request, 'tea/show.html', cloth_dict)

def cloth_imgs_show(request, cloth_id):

    cloth_imgs = ClothImg.objects.filter(cloth=cloth_id)
    cloth_dict = {
        'title': '衣服图片列表',
        'cloth_imgs': cloth_imgs,
    }
    return render(request, 'tea/show_imgs.html', cloth_dict)






# @login_required
# def cloth_upload(request):
#
#     if request.method == 'POST':
#         form = ClothUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             form_data = form.cleaned_data
#             cloth_design = ClothUpload(title=form_data['title'], content=form_data['content'],
#                                        price=form_data['price'], color=form_data['color'],
#                                        front_img=form_data['front_img'], back_img=form_data['back_img'],
#                                        user=request.user)
#             cloth_design.save()
#             return HttpResponse(cloth_design.id)
#         return HttpResponse('None')
#     else:
#         form = ClothUploadForm()
#         form_dict = {
#             'form': form,
#         }
#         return render(request, 'tea/design_cloth_form.html', form_dict)





# class reg_form(object):
#     error = ''
#     valid = False
#
#     def __init__(self, POST):
#         self.username = POST['username']
#         self.password = POST['password']
#         self.email = POST['email']
#
#         # to do, check validation
#         self.valid = True
#
#     def is_valid(self):
#         return self.valid
#
# def register_a(request):
#
#     if request.method == 'POST':
#         form = reg_form(request.POST)
#         if form.is_valid():
#             user = User.objects.create_user(form.username, form.email, form.password)
#             if user is not None:
#                 user.save()
#                 return HttpResponse('ok')
#         return HttpResponse('None')
#     else:
#         return render(request, 'tea/register.html', None)







#
# def register(request):
#
#     if 'POST' == request.method:
#         username = request.POST['username']
#         password = request.POST['password']
#         email = request.POST['email']
#         user = User.objects.create_user(username, email, password)
#         if user is not None:
#             user.save()
#             data = serializers.serialize('json', {'msg': 'ok'})
#             return HttpResponse(data)
#         else:
#             data = serializers.serialize('json', {'msg': 'failed'})
#             return HttpResponse(data)
#
#
# def login_user(request):
#
#     if 'POST' == request.method:
#         username = request.POST['username']
#         password = request.POST['password']
#         user = authenticate(username=username, password=password)
#         if user is not None:
#             if user.is_active:
#                 login(request, user)
#                 # return HttpResponseRedirect()
#             else:
#                 pass
#
#
# def logout_user(request):
#
#     logout(request)