<<<<<<< HEAD
# 2023-tieba-zk
=======
# 百科系统 (Baike System)

一个基于Django + Vue 3的现代化百科系统，提供完整的词条管理、用户认证和搜索功能。

## 项目特性

- **后端框架**: Django 4.2 + Django REST Framework
- **前端框架**: Vue 3 + Composition API+React数据可视化
- **数据库**: SQLite (开发环境)
- **认证系统**: Django内置认证 + Token认证
- **UI组件**: Ant Design Vue
- **状态管理**: Pinia
- **路由管理**: Vue Router 4

## 项目结构

```
baike/
├── baike/                 # Django项目配置
├── encyclopedia/          # 百科应用模块
├── users/                 # 用户认证应用
├── unified-frontend/      # Vue统一前端项目
├── static/                # 静态文件目录
├── db.sqlite3            # SQLite数据库
├── requirements.txt      # Python依赖
├── run.py               # 项目启动脚本
├── install.bat          # Windows安装脚本
└── README.md            # 项目说明
```

## 快速开始

### 1. 环境准备

确保已安装:
- Python 3.8+
- Node.js 16+

### 2. 一键安装 (Windows)

双击运行 `install.bat` 脚本，自动完成所有依赖安装和数据库初始化。

### 3. 手动安装

#### 后端安装

```bash
# 安装Python依赖
pip install -r requirements.txt

# 数据库迁移
python manage.py makemigrations
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

#### 前端安装

```bash
cd unified-frontend

# 安装依赖
npm install

# 返回项目根目录
cd ..
```

### 4. 启动项目

#### 方式一：一键启动
```bash
python run.py
```

#### 方式二：分别启动
```bash
# 终端1：启动后端
python manage.py runserver

# 终端2：启动前端
cd unified-frontend
npm run dev
```

## 访问地址

- **前端应用**: http://localhost:3000
- **后端API**: http://localhost:8000
- **管理后台**: http://localhost:8000/admin
- **API文档**: http://localhost:8000/api/

## 核心功能

### 词条管理
- 创建、编辑、删除词条
- 词条分类管理
- 词条搜索和筛选
- 词条详情查看
- 词条统计信息

### 用户系统
- 用户注册、登录、登出
- 个人资料管理
- 密码修改
- 权限控制

### 搜索功能
- 实时搜索词条标题和内容
- 搜索结果分页显示
- 搜索历史记录

### 分类系统
- 分类创建和管理
- 分类关联词条
- 分类统计信息

## API接口

### 词条相关
- `GET /api/entries/` - 获取词条列表（支持搜索参数）
- `POST /api/entries/` - 创建词条
- `GET /api/entries/{id}/` - 获取词条详情
- `PUT /api/entries/{id}/` - 更新词条
- `DELETE /api/entries/{id}/` - 删除词条

### 用户认证
- `POST /api/auth/register/` - 用户注册
- `POST /api/auth/login/` - 用户登录
- `POST /api/auth/logout/` - 用户登出
- `GET /api/auth/profile/` - 获取用户资料

### 分类管理
- `GET /api/categories/` - 获取分类列表
- `POST /api/categories/` - 创建分类

### 统计信息
- `GET /api/encyclopedia/statistics/` - 获取系统统计信息

## 技术架构

### 前端技术栈
- **框架**: Vue 3 + Composition API
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **UI组件**: Ant Design Vue
- **HTTP客户端**: Axios
- **构建工具**: Vite

### 后端技术栈
- **框架**: Django 4.2
- **API框架**: Django REST Framework
- **数据库**: SQLite
- **认证**: Django内置认证 + Token认证
- **跨域**: django-cors-headers

## 开发指南

### 前端开发
```bash
cd unified-frontend
npm run dev  # 开发模式
npm run build  # 生产构建
npm run lint  # 代码检查
```

### 后端开发
```bash
# 启动开发服务器
python manage.py runserver

# 创建数据库迁移
python manage.py makemigrations

# 应用迁移
python manage.py migrate

# 创建超级用户
python manage.py createsuperuser
```

## 部署说明

### 开发环境
- 使用SQLite数据库
- 启用DEBUG模式
- 使用开发服务器

### 生产环境建议
1. 设置环境变量
```bash
DEBUG=False
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:pass@host/dbname
```

2. 使用生产级Web服务器（如Gunicorn + Nginx）
3. 配置静态文件服务
4. 使用PostgreSQL数据库

## 故障排除

### 常见问题

1. **端口占用**: 确保8000和3000端口未被占用
2. **依赖安装失败**: 检查Python和Node.js版本
3. **数据库错误**: 运行 `python manage.py migrate` 重新迁移
4. **前端热重载失败**: 重启前端开发服务器

### 获取帮助
- 查看控制台错误信息
- 检查浏览器开发者工具
- 查看Django日志输出

## 许可证

MIT License

---

**注意**: 本项目为教学演示用途，生产环境使用请进行适当的安全配置和性能优化。
>>>>>>> 1ed1c59 (添加百科系统界面图HTML文件)
