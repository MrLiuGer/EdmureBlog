#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def article_all(arg_dict):
    article_type_id = arg_dict['article_type_id']
    category_id = arg_dict['category_id']
    tags__nid = arg_dict['tags__nid']
    p = arg_dict['p']
    url = reverse('article', kwargs={'article_type_id': 0, 'category_id':category_id, 'tags__nid':tags__nid})
    if article_type_id == '0':
        temp = '<a class="active" href="%s?p=%s">全部</a>' % (url,p,)
    else:
        temp = '<a href="%s?p=%s">全部</a>' % (url,p,)
    return mark_safe(temp)


@register.simple_tag
def article_combine(obj_list, arg_dict):
    li = []
    article_type_id = arg_dict['article_type_id']
    category_nid = arg_dict['category_id']
    tags__nid = arg_dict['tags__nid']
    p = arg_dict['p']
    for obj in obj_list:
        url = reverse('article', kwargs={'article_type_id': obj['nid'], 'category_id': category_nid, 'tags__nid':tags__nid})
        if obj['nid'] == int(article_type_id):
            temp = '<a class="active" href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        else:
            temp = '<a href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        li.append(temp)
    return mark_safe(''.join(li))


@register.simple_tag
def category_all(arg_dict):
    article_type_id = arg_dict['article_type_id']
    category_nid = arg_dict['category_id']
    tags__nid = arg_dict['tags__nid']
    p = arg_dict['p']
    url = reverse('article', kwargs={'article_type_id': article_type_id, 'category_id': 0, 'tags__nid':tags__nid})
    if category_nid == '0':
        temp = '<a class="active" href="%s?p=%s">全部</a>' % (url,p,)
    else:
        temp = '<a href="%s?p=%s">全部</a>' % (url,p,)
    return mark_safe(temp)

@register.simple_tag
def category_combine(obj_list, arg_dict):
    li = []
    article_type_id = arg_dict['article_type_id']
    category_nid = arg_dict['category_id']
    tags__nid = arg_dict['tags__nid']
    p = arg_dict['p']
    for obj in obj_list:
        url = reverse('article', kwargs={'article_type_id': article_type_id, 'category_id': obj['nid'], 'tags__nid':tags__nid})
        if obj['nid'] == int(category_nid):
            temp = '<a class="active" href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        else:
            temp = '<a href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        li.append(temp)
    return mark_safe(''.join(li))

@register.simple_tag
def tage_all(arg_dict):
    article_type_id = arg_dict['article_type_id']
    category_nid = arg_dict['category_id']
    tags__nid = arg_dict['tags__nid']
    p = arg_dict['p']
    url = reverse('article', kwargs={'article_type_id': article_type_id, 'category_id':category_nid, 'tags__nid':0 })
    if tags__nid == '0':
        temp = '<a class="active" href="%s?p=%s">全部</a>' % (url,p,)
    else:
        temp = '<a href="%s?p=%s">全部</a>' % (url,p,)
    return mark_safe(temp)


@register.simple_tag
def tage_combine(obj_list, arg_dict):
    li = []
    article_type_id = arg_dict['article_type_id']
    category_nid = arg_dict['category_id']
    tags__nid = arg_dict['tags__nid']
    p = arg_dict['p']
    for obj in obj_list:
        url = reverse('article', kwargs={'article_type_id': article_type_id, 'category_id': category_nid, 'tags__nid':obj['nid']})
        if obj['nid'] == int(tags__nid):
            temp = '<a class="active" href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        else:
            temp = '<a href="%s?p=%s">%s</a>' % (url,p, obj['title'])
        li.append(temp)
    return mark_safe(''.join(li))
