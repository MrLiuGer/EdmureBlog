#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.shortcuts import render
from django.shortcuts import redirect
from repository import models
from utils.pagination import Pagination
from django.urls import reverse
from django.db.models import Count
from django.db.models import F



def index(request, *args, **kwargs):
    """
    博客首页，展示全部博文
    :param request:

    :return:
    """
    # return render(request,'index.html')
    # 获取文章类型
    article_type_list = models.Article.type_choices
    # {},[]
    if kwargs:
        article_type_id = int(kwargs['article_type_id'])
        base_url = reverse('index', kwargs=kwargs)  # all/1.html
    else:
        article_type_id = None
        base_url = '/'  # /

    data_count = models.Article.objects.filter(**kwargs).count()

    page_obj = Pagination(request.GET.get('page'), data_count)
    article_list = models.Article.objects.filter(**kwargs).order_by('-nid')[page_obj.start:page_obj.end]
    page_str = page_obj.page_str(base_url)

    return render(
        request,
        'index.html',
        {
            'article_list': article_list,
            'article_type_id': article_type_id,
            'article_type_list': article_type_list,
            'page_str': page_str,
        }
    )


def home(request, site):
    """个人主页"""
    blog = models.Blog.objects.filter(site=site).first()
    # Article 连接category通过category_id where blog_id=blog.nid 文章分类表
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title', ).annotate(
        c=Count('nid'))
    tag_list = models.Tag.objects.filter(blog=blog).values('nid', 'title').annotate(c=Count('nid'))
    date_list = models.Article.objects.filter(blog=blog).extra(
        # select={'c': "date_format(create_time,'%%Y年%%m月')"}).values('c').annotate(ct=Count('nid'))
        select={'c': "strftime('%%Y年%%m月',create_time)"}).values('c').annotate(ct=Count('nid'))
    all_count = blog.article_set.all().count() if blog else 0
    urls = request.path_info
    page_info = Pagination(request.GET.get('page'), all_count, 5, 5)
    page_str = page_info.page_str(urls)
    article_list = blog.article_set.filter(blog=blog).all()[page_info.start:page_info.end] if blog else ''
    if not blog:
        return redirect('/')
    return render(request, "home.html",
                  {"blog": blog,
                   'article_list': article_list,
                   'page_str': page_str,
                   'category_list': category_list,
                   'tag_list': tag_list,
                   "date_list": date_list
                   })


def filter(request, site, condition, val):
    """个人主页筛选"""
    blog = models.Blog.objects.filter(site=site).first()
    if not blog:
        return redirect('/')
    tag_list = models.Tag.objects.filter(blog=blog).values('nid', 'title').annotate(c=Count('nid'))
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title', ).annotate(
        c=Count('nid'))
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'c': "strftime('%%Y年%%m月',create_time)"}).values('c').annotate(ct=Count('nid'))
    if condition == 'tag':
        all_count = models.Article.objects.filter(tags=val, blog=blog).all().count()
        urls = request.path_info
        page_info = Pagination(request.GET.get('page'), all_count, 5, 5)
        article_list = models.Article.objects.filter(tags__nid=1,blog=blog).all()[page_info.start:page_info.end]
        print('zxzxzxccz',val,article_list)
        page_str = page_info.page_str(urls)
    elif condition == 'category':
        all_count = models.Article.objects.filter(category_id=val, blog=blog).all().count()
        urls = request.path_info
        page_info = Pagination(request.GET.get('page'), all_count, 5, 5)
        article_list = models.Article.objects.filter(category_id=val, blog=blog).all()[
                       page_info.start:page_info.end]
        page_str = page_info.page_str(urls)
    elif condition == 'date':

        all_count = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y年%%m月", create_time)=%s'], params=[val, ]).all().count()
        urls = request.path_info
        page_info = Pagination(request.GET.get('page'), all_count, 5, 5)
        article_list = models.Article.objects.filter(blog=blog).extra(
            where=['strftime("%%Y年%%m月",create_time)=%s'], params=[val, ]).all()[page_info.start:page_info.end]
        # select * from tb where blog_id=1 and strftime("%Y-%m",create_time)=2017-01
        page_str = page_info.page_str(urls)
    else:
        article_list = []
        page_str = ''

    return render(
        request,
        'home_summary_list.html',
        {
            'blog': blog,
            'tag_list': tag_list,
            'category_list': category_list,
            'date_list': date_list,
            'article_list': article_list,
            "page_str": page_str,
        }
    )


def detailed(request, site, nid):
    """文章详细显示"""
    blog = models.Blog.objects.filter(site=site).first()
    tag_list = models.Tag.objects.filter(blog=blog).values('nid', 'title').annotate(c=Count('nid'))
    category_list = models.Article.objects.filter(blog=blog).values('category_id', 'category__title', ).annotate(
        c=Count('nid'))
    date_list = models.Article.objects.filter(blog=blog).extra(
        select={'c': "strftime('%%Y年%%m月',create_time)"}).values('c').annotate(ct=Count('nid'))
    article = models.Article.objects.filter(blog=blog, nid=nid).select_related('category', 'articledetail').first()
    return render(request, 'home_datailed.html',
                  {
                      'blog': blog,
                      'article': article,
                      'tag_list': tag_list,
                      'category_list': category_list,
                      'date_list': date_list,
                  }
                  )


def topdown(request):
    """顶或踩"""
    # 登录的用户
    username = request.session.get('username')
    # 点赞1还是踩0
    option_type = request.POST.get('tid')
    # 正在点赞或者踩的文章id
    article_id = request.POST.get("nid")
    message = ""
    # 判断是否登录
    if not username:
        message = '先登录'
        return HttpResponse(message)
    user_id = models.UserInfo.objects.filter(username=username).first().nid
    obj = models.UpDown.objects.filter(user_id=user_id, article_id=article_id).first()
    # 判断是否已经点赞或者踩过
    if obj:
        message = "你已经" + "赞过了" if obj.up else "踩过了"
    else:
        res = models.Article.objects.filter(nid=article_id, blog__user__nid=user_id).values('nid').first()
        if res:
            message = "不能为自己" + ("点赞" if int(option_type) else "踩")
        # 先创建一条点赞或者踩的数据记录
        models.UpDown.objects.create(up=option_type, article_id=article_id, user_id=user_id)
        # 再更新文章表里的点赞或者踩的数量

        option_key = {"up_count": F("up_count") + 1} if int(option_type) else {"down_count": F("down_count") + 1}
        models.Article.objects.filter(nid=article_id).update(**option_key)
    return HttpResponse(message)
