import json

from django.http import Http404

from .serializers import PostSerializer
from .models import Post
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status


# Create your views here.

class PostView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        id = self.request.POST.get('id')
        delete_flag = self.request.POST.get('delete_flag')
        if delete_flag:
            snippet = self.get_object(id)
            snippet.delete()
            data = list(self.request.data)
            return Response(data=data, status=status.HTTP_200_OK)
        elif id:
            snippet = self.get_object(id)
            posts_serializer = PostSerializer(snippet, data=request.data)
            if posts_serializer.is_valid():
                posts_serializer.save()
                return Response(posts_serializer.data, status=status.HTTP_200_OK)
            else:
                print('error', posts_serializer.errors)
                return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            posts_serializer = PostSerializer(data=request.data)
            if posts_serializer.is_valid():
                posts_serializer.save()
                return Response(posts_serializer.data, status=status.HTTP_201_CREATED)
            else:
                print('error', posts_serializer.errors)
                return Response(posts_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UploadFile(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def post(self, request, *args, **kwargs):
        files = self.request.FILES
        if files:
            data = {'status': 'ok'}
            return Response(data=data, status=status.HTTP_201_CREATED)
        else:
            print('error', )
            return Response('posts_serializer.errors', status=status.HTTP_400_BAD_REQUEST)
