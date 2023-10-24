from api import models
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
class BlogAuthentication(BaseAuthentication):

    def authenticate(self, request):
        token=request.query_params.get('token')
        if not token:
            return
        instance=models.UserInfo.objects.filter(token=token).first()
        if not instance:
            return

        return instance,token

    def authenticate_header(self, request):


        return "API"


class NoAuthentication(BaseAuthentication):

    def authenticate(self, request):

        return exceptions.AuthenticationFailed({"code":2000,"error":"认证失败"})

    def authenticate_header(self, request):

        return "API"