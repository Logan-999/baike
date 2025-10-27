#!/usr/bin/env python3
"""
百科系统启动脚本
支持一键启动后端和Vue前端
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def check_dependencies():
    """检查必要的依赖是否安装"""
    print("检查依赖...")
    
    # 检查Python
    try:
        import django
        print("✓ Django 已安装")
    except ImportError:
        print("✗ Django 未安装，请运行: pip install -r requirements.txt")
        return False
    
    # 检查Node.js
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ Node.js {result.stdout.strip()}")
        else:
            print("✗ Node.js 未安装")
            return False
    except FileNotFoundError:
        print("✗ Node.js 未安装")
        return False
    
    return True

def setup_backend():
    """设置并启动Django后端"""
    print("\n设置Django后端...")
    
    # 检查数据库迁移
    if not Path("db.sqlite3").exists():
        print("执行数据库迁移...")
        subprocess.run([sys.executable, 'manage.py', 'makemigrations'], check=True)
        subprocess.run([sys.executable, 'manage.py', 'migrate'], check=True)
        print("✓ 数据库迁移完成")
    
    # 创建超级用户（如果不存在）
    if not Path("superuser_created.flag").exists():
        print("创建超级用户...")
        try:
            subprocess.run([
                sys.executable, 'manage.py', 'createsuperuser', 
                '--username', 'admin', '--email', 'admin@baike.com', '--noinput'
            ], check=True)
            # 设置密码
            from django.contrib.auth import get_user_model
            User = get_user_model()
            admin_user = User.objects.get(username='admin')
            admin_user.set_password('admin123')
            admin_user.save()
            Path("superuser_created.flag").touch()
            print("✓ 超级用户创建完成 (用户名: admin, 密码: admin123)")
        except Exception as e:
            print(f"⚠ 创建超级用户失败: {e}")
    
    return True

def start_backend():
    """启动Django开发服务器"""
    print("\n启动Django后端服务器...")
    backend_process = subprocess.Popen([
        sys.executable, 'manage.py', 'runserver', '8000'
    ])
    
    # 等待服务器启动
    time.sleep(3)
    print("✓ Django后端服务器已启动: http://localhost:8000")
    print("  管理后台: http://localhost:8000/admin")
    print("  API文档: http://localhost:8000/api/docs/")
    
    return backend_process

def install_frontend_deps():
    """安装前端依赖"""
    print("\n安装前端依赖...")
    
    # 检查npm是否可用
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ npm命令未找到，请先安装Node.js")
        print("  下载地址: https://nodejs.org/")
        return False
    
    if not Path("unified-frontend", "node_modules").exists():
        os.chdir("unified-frontend")
        result = subprocess.run(['npm', 'install'], capture_output=True, text=True)
        os.chdir("..")
        
        if result.returncode == 0:
            print("✓ 前端依赖安装完成")
            return True
        else:
            print("✗ 前端依赖安装失败")
            print(result.stderr)
            return False
    else:
        print("✓ 前端依赖已存在")
        return True

def start_frontend():
    """启动前端开发服务器"""
    print("\n启动前端服务器...")
    
    # 检查npm是否可用
    try:
        subprocess.run(['npm', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ npm命令未找到，无法启动前端服务器")
        return None
    
    os.chdir("unified-frontend")
    frontend_process = subprocess.Popen([
        'npm', 'run', 'dev'
    ])
    os.chdir("..")
    
    time.sleep(5)  # 给前端服务器更多时间启动
    print("✓ 前端服务器已启动: http://localhost:3000")
    
    return frontend_process

def main():
    """主函数"""
    print("=" * 50)
    print("百科项目启动脚本")
    print("=" * 50)
    
    # 检查当前目录
    if not Path("manage.py").exists():
        print("错误: 请在项目根目录运行此脚本")
        sys.exit(1)
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    processes = []
    
    try:
        # 设置后端
        if not setup_backend():
            sys.exit(1)
        
        # 启动后端
        backend_process = start_backend()
        processes.append(backend_process)
        
        # 安装前端依赖
        if install_frontend_deps():
            # 启动前端
            frontend_process = start_frontend()
            processes.append(frontend_process)
        
        print("\n" + "=" * 50)
        print("所有服务已启动!")
        print("访问地址:")
        print("  前端应用: http://localhost:3000")
        print("  后端API: http://localhost:8000")
        print("  管理后台: http://localhost:8000/admin")
        print("\n按 Ctrl+C 停止所有服务")
        print("=" * 50)
        
        # 等待用户中断
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n正在停止所有服务...")
    
    finally:
        # 清理进程
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                process.kill()
        print("所有服务已停止")

if __name__ == "__main__":
    main()