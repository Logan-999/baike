@echo off
echo ================================
echo 百科系统安装脚本
echo ================================

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.8+
    pause
    exit /b 1
)

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Node.js，请先安装Node.js 16+
    pause
    exit /b 1
)

echo.
echo 1. 安装Python依赖...
pip install -r requirements.txt
if errorlevel 1 (
    echo 错误: Python依赖安装失败
    pause
    exit /b 1
)

echo.
echo 2. 安装前端依赖...
cd unified-frontend
npm install
if errorlevel 1 (
    echo 错误: 前端依赖安装失败
    pause
    exit /b 1
)
cd ..

echo.
echo 3. 初始化数据库...
python manage.py makemigrations
python manage.py migrate

echo.
echo 4. 创建超级用户...
python manage.py createsuperuser --username admin --email admin@baike.com --noinput
python -c "
from django.contrib.auth import get_user_model
User = get_user_model()
try:
    user = User.objects.get(username='admin')
    user.set_password('admin123')
    user.save()
    print('超级用户创建成功: 用户名: admin, 密码: admin123')
except Exception as e:
    print('创建超级用户失败:', e)
"

echo.
echo ================================
echo 安装完成！
echo ================================
echo.
echo 运行项目:
echo   1. 一键启动: python run.py
echo   2. 或分别启动:
echo      - 后端: python manage.py runserver
echo      - 前端: cd unified-frontend && npm run dev
echo.
echo 访问地址:
echo   前端应用: http://localhost:3000
echo   后端API: http://localhost:8000
echo   管理后台: http://localhost:8000/admin
echo.
echo 注意: 请确保端口3000和8000未被占用
echo.
pause