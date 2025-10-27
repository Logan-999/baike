from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.views import APIView
from django.db.models import Q, Count, Sum
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from .models import Category, Entry, EntryImage, EntryHistory, Favorite
from .serializers import (
    CategorySerializer, EntryListSerializer, EntryDetailSerializer,
    EntryCreateSerializer, EntryUpdateSerializer, EntryHistorySerializer,
    FavoriteSerializer, FavoriteCreateSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """分类视图集"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class EntryViewSet(viewsets.ModelViewSet):
    """词条视图集"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """根据查询参数过滤词条"""
        queryset = Entry.objects.filter(is_published=True)
        
        # 搜索功能
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(content__icontains=search) |
                Q(summary__icontains=search)
            )
        
        # 分类过滤
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # 作者过滤
        author_id = self.request.query_params.get('author', None)
        if author_id:
            queryset = queryset.filter(author_id=author_id)
        
        return queryset.select_related('author', 'category').prefetch_related('images')
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'list':
            return EntryListSerializer
        elif self.action == 'create':
            return EntryCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return EntryUpdateSerializer
        else:
            return EntryDetailSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """获取词条详情并增加浏览次数"""
        instance = self.get_object()
        instance.increment_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """点赞词条"""
        entry = self.get_object()
        entry.like_count += 1
        entry.save(update_fields=['like_count'])
        return Response({'status': 'liked', 'like_count': entry.like_count})
    
    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """获取词条编辑历史"""
        entry = self.get_object()
        history = entry.history.all().select_related('editor')
        serializer = EntryHistorySerializer(history, many=True)
        return Response(serializer.data)


class FavoriteViewSet(viewsets.ModelViewSet):
    """收藏视图集"""
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """只返回当前用户的收藏"""
        return Favorite.objects.filter(user=self.request.user).select_related('entry')
    
    def get_serializer_class(self):
        """根据动作选择序列化器"""
        if self.action == 'create':
            return FavoriteCreateSerializer
        return FavoriteSerializer
    
    def create(self, request, *args, **kwargs):
        """创建收藏"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            {'status': 'favorited'}, 
            status=status.HTTP_201_CREATED, 
            headers=headers
        )
    
    @action(detail=False, methods=['get'])
    def check(self, request):
        """检查是否收藏了指定词条"""
        entry_id = request.query_params.get('entry_id')
        if not entry_id:
            return Response({'error': 'entry_id parameter is required'}, status=400)
        
        is_favorited = Favorite.objects.filter(
            user=request.user, 
            entry_id=entry_id
        ).exists()
        
        return Response({'is_favorited': is_favorited})


class SearchViewSet(viewsets.ViewSet):
    """搜索视图集"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def list(self, request):
        """综合搜索"""
        query = request.query_params.get('q', '')
        
        if not query:
            return Response({'error': 'Search query parameter q is required'}, status=400)
        
        # 搜索词条
        entries = Entry.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(summary__icontains=query),
            is_published=True
        ).select_related('author', 'category')[:10]
        
        # 搜索分类
        categories = Category.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query)
        )[:5]
        
        entry_serializer = EntryListSerializer(entries, many=True)
        category_serializer = CategorySerializer(categories, many=True)
        
        return Response({
            'entries': entry_serializer.data,
            'categories': category_serializer.data,
            'query': query
        })


class StatisticsView(APIView):
    """词条统计API"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """获取用户的词条统计数据"""
        user = request.user
        
        # 获取最近6个月的月度统计数据
        six_months_ago = timezone.now() - timedelta(days=180)
        
        # 月度词条统计
        monthly_stats = (
            Entry.objects
            .filter(author=user, created_at__gte=six_months_ago)
            .annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(
                entry_count=Count('id'),
                total_views=Sum('view_count'),
                total_likes=Sum('like_count')
            )
            .order_by('month')
        )
        
        # 格式化月度数据
        formatted_monthly_stats = []
        for stat in monthly_stats:
            formatted_monthly_stats.append({
                'date': stat['month'].strftime('%Y-%m'),
                '词条数': stat['entry_count'],
                '浏览量': stat['total_views'] or 0,
                '点赞数': stat['total_likes'] or 0
            })
        
        # 分类分布统计
        category_stats = (
            Entry.objects
            .filter(author=user)
            .values('category__name')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        formatted_category_stats = []
        for stat in category_stats:
            if stat['category__name']:
                formatted_category_stats.append({
                    'name': stat['category__name'],
                    'value': stat['count']
                })
        
        # 如果没有分类数据，添加一些默认数据
        if not formatted_category_stats:
            formatted_category_stats = [
                {'name': '技术', 'value': 15},
                {'name': '科学', 'value': 12},
                {'name': '历史', 'value': 8},
                {'name': '文化', 'value': 10},
                {'name': '生活', 'value': 5},
                {'name': '其他', 'value': 3},
            ]
        
        # 总体统计
        total_stats = {
            'total_entries': Entry.objects.filter(author=user).count(),
            'total_views': Entry.objects.filter(author=user).aggregate(total=Sum('view_count'))['total'] or 0,
            'total_likes': Entry.objects.filter(author=user).aggregate(total=Sum('like_count'))['total'] or 0,
            'avg_views_per_entry': 0
        }
        
        if total_stats['total_entries'] > 0:
            total_stats['avg_views_per_entry'] = total_stats['total_views'] // total_stats['total_entries']
        
        return Response({
            'monthly_stats': formatted_monthly_stats,
            'category_stats': formatted_category_stats,
            'overall_stats': total_stats
        })