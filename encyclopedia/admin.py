from django.contrib import admin
from .models import Category, Entry, EntryImage, EntryHistory, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """分类管理"""
    list_display = ['name', 'description', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    ordering = ['name']


class EntryImageInline(admin.TabularInline):
    """词条图片内联管理"""
    model = EntryImage
    extra = 1
    fields = ['image', 'caption']


class EntryHistoryInline(admin.TabularInline):
    """编辑历史内联管理"""
    model = EntryHistory
    extra = 0
    readonly_fields = ['editor', 'old_content', 'new_content', 'edit_summary', 'edited_at']
    can_delete = False


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    """词条管理"""
    list_display = ['title', 'category', 'author', 'is_published', 'view_count', 'like_count', 'created_at']
    list_filter = ['category', 'is_published', 'created_at', 'author']
    search_fields = ['title', 'content', 'summary']
    readonly_fields = ['view_count', 'like_count', 'created_at', 'updated_at']
    ordering = ['-created_at']
    
    # 内联管理
    inlines = [EntryImageInline, EntryHistoryInline]
    
    # 字段分组
    fieldsets = [
        ('基本信息', {
            'fields': ['title', 'category', 'author', 'is_published']
        }),
        ('内容信息', {
            'fields': ['summary', 'content']
        }),
        ('统计信息', {
            'fields': ['view_count', 'like_count', 'created_at', 'updated_at']
        })
    ]
    
    def save_model(self, request, obj, form, change):
        """保存模型时自动设置作者"""
        if not change:  # 新建时设置作者
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(EntryImage)
class EntryImageAdmin(admin.ModelAdmin):
    """词条图片管理"""
    list_display = ['entry', 'caption', 'uploaded_at']
    list_filter = ['uploaded_at']
    search_fields = ['entry__title', 'caption']
    ordering = ['-uploaded_at']


@admin.register(EntryHistory)
class EntryHistoryAdmin(admin.ModelAdmin):
    """编辑历史管理"""
    list_display = ['entry', 'editor', 'edit_summary', 'edited_at']
    list_filter = ['edited_at', 'editor']
    search_fields = ['entry__title', 'editor__username', 'edit_summary']
    readonly_fields = ['entry', 'editor', 'old_content', 'new_content', 'edit_summary', 'edited_at']
    ordering = ['-edited_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """收藏管理"""
    list_display = ['user', 'entry', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'entry__title']
    ordering = ['-created_at']