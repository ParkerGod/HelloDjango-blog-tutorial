#!/usr/bin/env python
import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blogproject.settings.local')
os.environ['ENABLE_HAYSTACK_REALTIME_SIGNAL_PROCESSOR'] = 'no'

import django
django.setup()

from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from django.utils import timezone

# 创建测试用户
user, created = User.objects.get_or_create(username='testuser', defaults={'email': 'test@example.com'})
if created:
    user.set_password('testpass')
    user.save()
    print('Created user: testuser')
else:
    print('User already exists: testuser')

# 创建分类
category, created = Category.objects.get_or_create(name='技术')
if created:
    print('Created category: 技术')
else:
    print('Category already exists: 技术')

# 创建标签
tag1, created1 = Tag.objects.get_or_create(name='Python')
if created1:
    print('Created tag: Python')
tag2, created2 = Tag.objects.get_or_create(name='Django')
if created2:
    print('Created tag: Django')

# 创建测试文章
for i in range(1, 15):
    post, created = Post.objects.get_or_create(
        title=f'测试文章 {i}',
        defaults={
            'body': f'这是第 {i} 篇测试文章的内容。\n\n## 章节一\n\n这里是正文内容，支持 **Markdown** 格式。',
            'category': category,
            'author': user,
            'modified_time': timezone.now(),
        }
    )
    if created:
        post.tags.add(tag1)
        if i % 2 == 0:
            post.tags.add(tag2)
        print(f'Created post: {post.title}')

print(f'\nTotal posts: {Post.objects.count()}')
print(f'Total categories: {Category.objects.count()}')
print(f'Total tags: {Tag.objects.count()}')
