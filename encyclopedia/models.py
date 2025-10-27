from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """百科分类模型"""
    name = models.CharField(max_length=100, unique=True, verbose_name='分类名称')
    description = models.TextField(blank=True, verbose_name='分类描述')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    
    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Entry(models.Model):
    """百科词条模型"""
    title = models.CharField(max_length=200, unique=True, verbose_name='词条标题')
    content = models.TextField(verbose_name='词条内容')
    summary = models.TextField(max_length=500, blank=True, verbose_name='摘要')
    
    # 关联字段
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name='分类'
    )
    author = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='创建者'
    )
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    # 状态字段
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    
    # 统计字段
    view_count = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    like_count = models.PositiveIntegerField(default=0, verbose_name='点赞数')
    
    class Meta:
        verbose_name = '词条'
        verbose_name_plural = '词条'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['title']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['author']),
        ]
    
    def __str__(self):
        return self.title
    
    def increment_view_count(self):
        """增加浏览次数"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class EntryImage(models.Model):
    """词条图片模型"""
    entry = models.ForeignKey(
        Entry, 
        on_delete=models.CASCADE, 
        related_name='images',
        verbose_name='所属词条'
    )
    image = models.ImageField(upload_to='encyclopedia/images/', verbose_name='图片')
    caption = models.CharField(max_length=200, blank=True, verbose_name='图片说明')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='上传时间')
    
    class Meta:
        verbose_name = '词条图片'
        verbose_name_plural = '词条图片'
    
    def __str__(self):
        return f"{self.entry.title} - {self.caption or '图片'}"


class EntryHistory(models.Model):
    """词条编辑历史模型"""
    entry = models.ForeignKey(
        Entry, 
        on_delete=models.CASCADE, 
        related_name='history',
        verbose_name='所属词条'
    )
    editor = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='编辑者'
    )
    old_content = models.TextField(verbose_name='原内容')
    new_content = models.TextField(verbose_name='新内容')
    edit_summary = models.CharField(max_length=200, blank=True, verbose_name='编辑摘要')
    edited_at = models.DateTimeField(auto_now_add=True, verbose_name='编辑时间')
    
    class Meta:
        verbose_name = '编辑历史'
        verbose_name_plural = '编辑历史'
        ordering = ['-edited_at']
    
    def __str__(self):
        return f"{self.entry.title} - {self.editor.username} - {self.edited_at}"


class Favorite(models.Model):
    """用户收藏模型"""
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        verbose_name='用户'
    )
    entry = models.ForeignKey(
        Entry, 
        on_delete=models.CASCADE, 
        verbose_name='词条'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收藏时间')
    
    class Meta:
        verbose_name = '收藏'
        verbose_name_plural = '收藏'
        unique_together = ['user', 'entry']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} 收藏了 {self.entry.title}"