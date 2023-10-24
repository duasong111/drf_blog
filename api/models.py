from django.db import models


# Create your models here.
class UserInfo(models.Model):
    username = models.CharField(verbose_name="用户名", max_length=64, db_index=True)
    password = models.IntegerField(verbose_name="密码")
    token = models.CharField(verbose_name="TOKEN", max_length=64, null=True, blank=True)


class Blog(models.Model):
    category_choice = ((1, "云计算"), (2, "Python开发"), (3, "C++"))
    category = models.IntegerField(verbose_name="分类", choices=category_choice)

    image = models.CharField(verbose_name="封面", max_length=255)
    title = models.CharField(verbose_name="标题", max_length=32)
    summary = models.CharField(verbose_name="简介", max_length=256)
    text = models.TextField(verbose_name="博文")
    ctime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
    creator = models.ForeignKey(verbose_name="创建者", to="UserInfo",
                                on_delete=models.CASCADE)
    comment_count = models.PositiveIntegerField(verbose_name="评论数", default=0)
    favor_count = models.PositiveIntegerField(verbose_name="喜欢数", default=0)


class Favor(models.Model):
    """赞"""
    blog = models.ForeignKey(verbose_name="咨询", to="Blog", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['blog', 'user'], name='uni_favor_blog_user')
        ]


class Comment(models.Model):
    """评论区"""
    blog = models.ForeignKey(verbose_name="博客", to="Blog", on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)

    content = models.CharField(verbose_name="内容", max_length=150)
    create_datetime = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)
