import uuid

from django.shortcuts import render, HttpResponse
from rest_framework.views import APIView
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import exceptions
from api import models
from ext.auth import BlogAuthentication,NoAuthentication


class BlogSerializers(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    creator_name = serializers.CharField(source="creator.username")

    class Meta:
        model = models.Blog
        fields = ["category", "image", "title", "summary", "ctime", "comment_count", "favor_count", "creator",
                  "creator_name"]

    def get_creator(self, obj):
        return {"id": obj.creator_id, "name": obj.creator.username}


class BlogView(APIView):
    def get(self, request, *args, **kwargs):
        queryset = models.Blog.objects.all().order_by("-id")
        # 进行序列化操作
        ser = BlogSerializers(instance=queryset, many=True)
        result = {
            "statue": 1000,
            "mes": "返回成功",
            "data": ser.data
        }
        return Response(result)


class BlogDetailSerializers(serializers.ModelSerializer):
    category = serializers.CharField(source="get_category_display")
    ctime = serializers.DateTimeField(format="%Y-%m-%d")
    creator_name = serializers.CharField(source="creator.username")

    class Meta:
        model = models.Blog
        fields = "__all__"


class BlogDatilView(APIView):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk")

        instance = models.Blog.objects.filter(id=pk).first()
        # 如果该用户不存在的情况系
        if not instance:
            return Response({"code": 1001, 'error': "不存在"})
        # 进行序列化的处理
        ser = BlogDetailSerializers(instance=instance, many=False)
        # 数据的返回
        context = {"code": 1000, "data": ser.data}

        return Response(context)


class CommentSerializers(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username")

    class Meta:
        model = models.Comment
        fields = ["id", "content", "user"]
        extra_kwargs = {
            "id":{"read_only":True},
            "user":{'ready_only':True}
        }
    # def nb_user(self,obj):
    #     return obj.user.username

class CommentView(APIView):
    authentication_classes = [BlogAuthentication, ]

    def get(self, request, *args, **kwargs):
        """评论列表"""
        # 根据传输过来的那个id来获取对用的评论，好使
        queryset = models.Comment.objects.filter(blog_id=kwargs.get('blog_id')).all()
        # 进行序列化的处理
        ser = CommentSerializers(instance=queryset, many=True)
        # 数据的返回
        context = {"code": 1000, "data": ser.data}

        return Response(context)

    def post(self, request, blog_id):
        """发布评论"""
        if not request.user:
            return Response({"code": 3000, "error": "认证失败"})
        blog_object = models.Blog.objects.filter(id=blog_id).first()
        if not blog_object:
            return Response({"code": 2000, "error": "博客不存在"})
        ser=CommentSerializers(data=request.data)

        if not ser.is_valid():
            return Response({"code": 1002, "error": "博客不存在","detail":ser.errors})

        ser.save(user=request.user,blog=blog_object)
        return Response({"code": 1000, "data":ser.data})

class RegisterSerializers(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["id", "username", "password", "confirm_password"]
        extra_kwargs = {
            "id": {"read_only": True},
            "password": {"write_only": True}
        }

    def validate_password(self, value):
        return value

    def validate_confirm_password(self, value):
        password = self.initial_data.get("password")
        if password != value:
            raise exceptions.ValidationError("密码不一样")
        return value


class RegistesView(APIView):
    """用户的注册窗口"""

    def post(self, request):
        # print(request.data)
        ser = RegisterSerializers(data=request.data)
        if ser.is_valid():
            ser.validated_data.pop("confirm_password")
            ser.save()
            return Response({"code": 200, "message": "成功", "data": ser.data})
        else:
            return Response({"code": 1000, "errors": "注册失败", "data": ser.errors})


class LoginSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["username", "password"]

class LoginView(APIView):
    def post(self, request):

        ser = LoginSerializers(data=request.data)
        if not ser.is_valid():
            return Response({"code": 1001, "error": "校验失败", "detail": ser.errors})

        instance = models.UserInfo.objects.filter(**ser.validated_data).first()
        if not instance:
            return Response({"code": 1001, "error": "用户名或密码错误"})

        token = str(uuid.uuid4())
        instance.token = token
        instance.save()

        return Response({"code": 200,"message":"登录成功", "token": token})



class FavorView(APIView):

    authentication_classes = [BlogAuthentication,NoAuthentication]

    def post(self,request):

        return Response("请求成功")
        pass






"""仅仅是为了添加数据的"""
def db(request):
    # v1 = models.UserInfo.objects.create(username="lili", password="1234")
    # v2 = models.UserInfo.objects.create(username="hh", password="456")
    #
    # models.Blog.objects.create(
    #     category=1,
    #     image="xxx/xxx.png",
    #     title="hhhh",
    #     text="saishaishasasa",
    #     creator=v1
    # )
    # models.Blog.objects.create(
    #     category=2,
    #     image="xxx/xxx.png",
    #     title="hhhh",
    #     text="哈哈哈哈哈哈",
    #     creator=v2
    # )
    # models.Comment.objects.create(content="不知道啊",blog_id=1,user_id=2)
    # models.Comment.objects.create(content="你是个狗吧", blog_id=1, user_id=1)

    return HttpResponse("成功")
