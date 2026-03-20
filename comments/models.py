from django.db import models
from django.utils import timezone


class Comment(models.Model):
    name = models.CharField('名字', max_length=50)
    email = models.EmailField('邮箱')
    url = models.URLField('网址', blank=True)
    text = models.TextField('内容')
    created_time = models.DateTimeField('创建时间', default=timezone.now)
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)
    parent = models.ForeignKey('self', verbose_name='父评论', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    level = models.PositiveIntegerField('嵌套层级', default=0, help_text='评论嵌套层级，最多3级')
    is_approved = models.BooleanField('审核状态', default=False, help_text='新评论默认待审核，管理员审核后显示')

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return '{}: {}'.format(self.name, self.text[:20])
