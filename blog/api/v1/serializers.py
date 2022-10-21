from rest_framework import serializers
from blog.models import Post, Category
from accounts.models import Profile



# class PostSerializer(serializers.Serializer):
#     id = serializers.IntegerField()
#     title = serializers.CharField(max_length=255)


class PostSerializer(serializers.ModelSerializer):
    #content = serializers.ReadOnlyField() #field ra readonly mikonad
    snippet  = serializers.ReadOnlyField(source='get_snippet')
    absolute_url = serializers.SerializerMethodField(method_name='get_abs_url')
    class Meta:
        model = Post
        fields = ['id', 'author', 'title', 'image', 'content', 'category', 'snippet', 'created_date', 'published_date', 'status', 'absolute_url']
        read_only_fields = ['author']

    def get_abs_url(self, obj):
        request = self.context.get('request')
        return request.build_absolute_uri(obj.pk)

    def to_representation(self, instance):
        request = self.context.get('request')
        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs').get('pk'): #ba in kar mifahmim pk darad ya na, tashkise list va object
            rep.pop('snippet', None)
            rep.pop('absolute_url', None)
        else:
            rep.pop('content')

        rep['category'] = CategorySerializer(instance.category, context={'request': request}).data
        return rep

    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get('request').user.id)
        return super().create(validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']