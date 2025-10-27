from rest_framework import serializers
from .models import Category, Entry, EntryImage, EntryHistory, Favorite
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """用户序列化器"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class CategorySerializer(serializers.ModelSerializer):
    """分类序列化器"""
    entry_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'entry_count', 'created_at']
    
    def get_entry_count(self, obj):
        """获取分类下的词条数量"""
        return obj.entry_set.count()


class EntryImageSerializer(serializers.ModelSerializer):
    """词条图片序列化器"""
    class Meta:
        model = EntryImage
        fields = ['id', 'image', 'caption', 'uploaded_at']


class EntryListSerializer(serializers.ModelSerializer):
    """词条列表序列化器"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    summary = serializers.CharField(read_only=True)
    
    class Meta:
        model = Entry
        fields = [
            'id', 'title', 'summary', 'category', 'author', 
            'created_at', 'updated_at', 'view_count', 'like_count'
        ]


class EntryDetailSerializer(serializers.ModelSerializer):
    """词条详情序列化器"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = EntryImageSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField()
    
    class Meta:
        model = Entry
        fields = [
            'id', 'title', 'content', 'summary', 'category', 'author',
            'created_at', 'updated_at', 'view_count', 'like_count',
            'is_published', 'images', 'is_favorited'
        ]
    
    def get_is_favorited(self, obj):
        """检查当前用户是否收藏了该词条"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Favorite.objects.filter(user=request.user, entry=obj).exists()
        return False


class EntryCreateSerializer(serializers.ModelSerializer):
    """词条创建序列化器"""
    class Meta:
        model = Entry
        fields = ['title', 'content', 'summary', 'category', 'is_published']
    
    def validate_title(self, value):
        """验证标题唯一性"""
        if Entry.objects.filter(title=value).exists():
            raise serializers.ValidationError("词条标题已存在")
        return value
    
    def create(self, validated_data):
        """创建词条"""
        request = self.context.get('request')
        validated_data['author'] = request.user
        return super().create(validated_data)


class EntryUpdateSerializer(serializers.ModelSerializer):
    """词条更新序列化器"""
    class Meta:
        model = Entry
        fields = ['title', 'content', 'summary', 'category', 'is_published']
    
    def update(self, instance, validated_data):
        """更新词条并记录编辑历史"""
        request = self.context.get('request')
        
        # 记录编辑历史
        EntryHistory.objects.create(
            entry=instance,
            editor=request.user,
            old_content=instance.content,
            new_content=validated_data.get('content', instance.content),
            edit_summary=f"更新词条内容"
        )
        
        return super().update(instance, validated_data)


class EntryHistorySerializer(serializers.ModelSerializer):
    """编辑历史序列化器"""
    editor = UserSerializer(read_only=True)
    
    class Meta:
        model = EntryHistory
        fields = ['id', 'editor', 'old_content', 'new_content', 'edit_summary', 'edited_at']


class FavoriteSerializer(serializers.ModelSerializer):
    """收藏序列化器"""
    entry = EntryListSerializer(read_only=True)
    
    class Meta:
        model = Favorite
        fields = ['id', 'entry', 'created_at']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    """收藏创建序列化器"""
    class Meta:
        model = Favorite
        fields = ['entry']
    
    def create(self, validated_data):
        """创建收藏"""
        request = self.context.get('request')
        validated_data['user'] = request.user
        
        # 检查是否已收藏
        if Favorite.objects.filter(user=request.user, entry=validated_data['entry']).exists():
            raise serializers.ValidationError("已收藏该词条")
        
        return super().create(validated_data)