from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """用户扩展资料模型"""
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name='profile',
        verbose_name='用户'
    )
    
    # 扩展字段
    bio = models.TextField(max_length=500, blank=True, verbose_name='个人简介')
    avatar = models.ImageField(
        upload_to='users/avatars/', 
        blank=True, 
        null=True,
        verbose_name='头像'
    )
    location = models.CharField(max_length=100, blank=True, verbose_name='所在地')
    website = models.URLField(max_length=200, blank=True, verbose_name='个人网站')
    
    # 统计字段
    entries_count = models.PositiveIntegerField(default=0, verbose_name='创建词条数')
    favorites_count = models.PositiveIntegerField(default=0, verbose_name='收藏数')
    
    # 时间字段
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} 的资料"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """创建用户时自动创建用户资料"""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """保存用户时自动保存用户资料"""
    instance.profile.save()