from django.shortcuts import render,redirect
from app01 import models
from functools import wraps
# Create your views here.
def check_login(func):
    @wraps(func)
    def wrapper(request,*args,**kwargs):
        if request.session.get('login')=='666':
            return func(request,*args,**kwargs)
        else:
            url=request.get_full_path()
            return redirect("/login/?next={}".format(url))
    return wrapper
@check_login
def book_list(request):
    # 1. 查询所有的书籍数
    data = models.Book.objects.all()
    # 统计下总数据条数
    total_num = data.count()
    # 从URL中提取出来当前访问的具体页码数
    current_page = request.GET.get("page")
    from utils import mypage
    page_obj = mypage.Page(total_num, current_page, 'book_list')
    # 当前页码应该展示的书籍数据
    book_list = data[page_obj.data_start:page_obj.data_end]
    # 生成分页的页码
    page_html = page_obj.page_html()
    # 2. 在页面上展示出来
    return render(request, "book_list.html", {"book_list": book_list, "page_html": page_html})

def login(request):
    error_msg = ''
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user_obj=models.User.objects.filter(username=username,password=password)
        if user_obj:
            request.session['login']='666'
            url=request.GET.get('next')
            if not url:
                url='/book_list/'
            return redirect(url)
        else:
            error_msg='username or password error'
    return  render(request,'login.html',{'error_msg':error_msg})
# from django.views import View
# from django.utils.decorators import method_decorator
#
# class Login(View):
#     def get(self,request):
#         return render(request,'login.html')
#     def post(self,request):
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user_obj=models.User.objects.filter(username=username,password=password)
#         if user_obj:
#             request.session['login']='666'
#             url=request.GET.get('next')
#             if url:
#                 return redirect(url)
#             return redirect('/book_list/')
#         else:
#             error_msg='username or password error'
#             return render(request,'login.html',{'error_msg':error_msg})
#
# class Book(View):
#     @method_decorator(check_login)
#     def get(self,request):
#         data=models.Book.objects.all()
#         total_num=data.count()
#         current_page=request.GET.get('page')
#         from utils import mypage
#         page_obj=mypage.Page(total_num,current_page,'book_list')
#         book_list=data[page_obj.data_start:page_obj.data_end]
#         page_html=page_obj.page_html()
#         return render(request,'book_list.html',{'book_list':book_list,'page_html':page_html})
#     def post(self,request):
#         request.session.flush()
#         return render(request,'login.html')
