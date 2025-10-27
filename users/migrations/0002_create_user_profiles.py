from django.db import migrations
from django.contrib.auth.models import User

def create_user_profiles(apps, schema_editor):
    """为所有现有用户创建UserProfile记录"""
    UserProfile = apps.get_model('users', 'UserProfile')
    User = apps.get_model('auth', 'User')
    
    for user in User.objects.all():
        # 检查是否已经存在UserProfile
        if not hasattr(user, 'profile'):
            UserProfile.objects.create(user=user)
            print(f"为用户 {user.username} 创建了UserProfile")

def reverse_create_user_profiles(apps, schema_editor):
    """回滚操作 - 删除所有UserProfile记录"""
    UserProfile = apps.get_model('users', 'UserProfile')
    UserProfile.objects.all().delete()

class Migration(migrations.Migration):
    dependencies = [
        ('users', '0001_initial'),
    ]
    
    operations = [
        migrations.RunPython(create_user_profiles, reverse_create_user_profiles),
    ]