from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import PostSerializer, CategorySerializer
from ...models import Post, Category
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import mixins
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .pagination import DefaultPagination

# @api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
# def post_list(request):
#     #posts = Post.objects.all()
#     if request.method == 'GET':
#         posts = Post.objects.filter(status=True)
#         setializer= PostSerializer(posts, many=True)
#         return Response(setializer.data)
#     elif request.method == 'POST':
#         serializer = PostSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         else:
#             return Response(serializer.errors)

class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)



# class PostList(APIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = PostSerializer
#
#     #amaliat marbut be get kardan ra handle mikonad
#     def get(self, request):
#         posts = Post.objects.filter(status=True)
#         setializer = PostSerializer(posts, many=True)
#         return Response(setializer.data)
#     def post(self, request):
#         serializer = PostSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)



# @api_view(['GET', 'PUT', 'DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly ])
# def post_detail(request, id):
#     # try:
#     #     post = Post.objects.get(pk=id)
#     #     serializer = PostSerializer(post)
#     #     return Response(serializer.data)
#     # except Post.DoesNotExist:
#     #     return Response('post does not exist!',status=status.HTTP_404_NOT_FOUND)
#     post = get_object_or_404(Post, pk=id, status=True)
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = PostSerializer(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#     elif request.method == 'DELETE':
#         post.delete()
#         return Response('item removed successfully')


# class PostDetail(APIView):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     serializer_class = PostSerializer
#
#     def get(self, request, id):
#         post = get_object_or_404(Post, pk=id, status=True)
#         serializer = self.serializer_class(post)
#         return Response(serializer.data)
#
#     def put(self, request, id):
#         post = get_object_or_404(Post, pk=id, status=True)
#         serializer = PostSerializer(post, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)
#
#     def delete(self, request, id):
#         post = get_object_or_404(Post, pk=id, status=True)
#         post.delete()
#         return Response({'detial': 'item removed successfully'}, status=status.HTTP_204_NO_CONTENT)

class PostDetail(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    lookup_field = 'id'



    # def get(self, request, id):
    #     post = get_object_or_404(Post, pk=id, status=True)
    #     serializer = self.serializer_class(post)
    #     return Response(serializer.data)

class PostModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    #chon az ModelViewset estefade kardim niazi be tarife dasti method nis
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category',  'author']
    search_fields = ['title', 'content']
    ordering_fields = ['created_date']
    pagination_class = DefaultPagination


class CategoryModelViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.all()