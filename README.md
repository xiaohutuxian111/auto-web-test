# Web UI 自动化测试项目

## **项目描述**

- 基于playwright 实现的自化测试项目,目标网址:[ARS经济运营管理系统](http://192.168.10.240:806/login)
- 本项目采用Page Object设计模式，实现了页面操作的封装和复用
- 支持数据驱动测试，使用YAML文件管理测试数据
- 集成了Allure报告，提供美观的测试报告展示

## 项目功能

- [x] 基本操作实现封装
- [x] 基于pytest实现页面的封装
- [x] 自动生成测试报告
- [x] 支持文件上传和下载操作
- [x] 支持表格数据验证和操作
- [x] 支持表单自动填写和验证
- [x] 支持飞书发送记录测试结果
- [ ] 使用jenkins 实现自动化继承
- [ ] 实现的页面测试覆盖率的计算
- [ ] 实现docker部署

## 基本要求

| **要素**     | **描述**           |
|------------|------------------|
| **python** | **uv包管理,版本3.11** |
| **浏览器驱动**  | **playwright**   |
| **测试框架**   | **pytest**       |
| **报告工具**   | **allure**       |

## 项目结构

```
auto-web-test/
├── .agents/               # Codex/Agent 项目技能与规则
│   └── skills/
├── .Auth/                 # 本地认证缓存，运行时生成
├── config/                 # 配置文件目录
│   ├── auth/               # 登录认证用户配置
│   │   └── test_users.yaml
│   ├── constants.py       # 常量与枚举
│   ├── database.py        # 数据库连接配置
│   └── settings.py        # 项目配置
├── docker/                # Docker 镜像与压测插件
├── docs/                  # 项目设计文档与文档图片
│   └── assets/            # README 和文档图片资源
├── requirements/          # Python 依赖清单
│   └── requirements.txt
├── scripts/               # CI、清理和辅助脚本
├── src/                   # 自动化测试源码
│   ├── core/              # 核心页面能力
│   ├── data_models/       # 测试数据模型
│   ├── interfaces/        # 接口辅助能力
│   ├── page_object/       # 页面对象
│   ├── test_cases/        # 测试用例
│   └── utils/             # 通用工具
├── pytest.ini             # pytest 配置文件
├── pyproject.toml         # 项目元数据
└── README.md              # 项目说明文档
```

## 目录说明

### 1. 核心模块 (src/core/)

- **locators.py**: 提供统一的元素定位方法
- **table.py**: 封装表格相关的操作
- **base_page.py**: 页面对象基类和通用页面动作
- **upload_file.py**: 封装文件上传和下载功能

### 2. 页面对象 (src/page_object/)

- **登录页.py**: 登录页面对象
- **pageIns.py**: 页面对象实例入口
- 其他页面类: 按业务模块分类，实现具体页面操作

### 3. 测试数据与认证配置

- **config/auth/test_users.yaml**: 存储登录认证用户信息，包括用户名、密码、租户和角色等
- **src/data_models/**: 存储结构化测试数据模型

### 4. 工具类 (src/utils/)

- **date_uitl.py**: 日期处理工具
- **log_util.py**: 日志记录工具
- **path_util.py**: 路径处理工具
- **check_util.py**: 数据检查工具
- **global_map.py**: 全局变量管理工具

### 5. 配置文件 (config/)

- **settings.py**: 项目配置信息，包括环境变量、URL等
- **database.py**: 数据库连接配置，包括数据库类型、地址、连接池和 SQLAlchemy URL
- **constants.py**: 常量和枚举定义

### 6. 测试用例 (test_cases/)

存放在 **src/test_cases/**，按业务模块分类组织

### 7. 文档资源 (docs/assets/)

存放 README 和设计文档引用的图片资源

### 8. 依赖文件 (requirements/)

存放 Python 依赖清单，Dockerfile 和本地安装命令共用同一路径

## 技术栈

- Python 3.11
- Playwright
- Pytest
- Allure
- YAML

## 主要功能

1. 基于Page Object模式的页面封装
2. 统一的元素定位策略
3. 完整的表单操作支持
4. 灵活的表格操作
5. 强大的搜索功能
6. 文件上传和下载功能
7. 完善的日志记录
8. 数据驱动测试支持
9. 美观的测试报告

## 使用说明

### 1. 环境准备：

   ```bash
   # 安装Python 3.11
   # 安装uv包管理工具
   pip install uv
   
   # 安装项目依赖
   uv pip install -r requirements/requirements.txt
   
   # 安装playwright浏览器
   playwright install
   ```

### 2. 运行测试：

   ```bash
   # 运行所有测试用例
   pytest src/test_cases/ --alluredir=./allure-results
   
   # 运行指定模块的测试用例
   pytest src/test_cases/test_module/ --alluredir=./allure-results
   
   # 运行指定测试用例
   pytest src/test_cases/test_module/test_file.py --alluredir=./allure-results
   ```

### 3. 查看报告：

   ```bash
   # 启动Allure报告服务
   allure serve ./allure-results
   
   # 生成静态报告
   allure generate ./allure-results -o ./allure-report
   ```

### 自动化进度报告[进度报告](https://vcn25s6jh1tk.feishu.cn/base/VRsxbSmHgaKD7jswAAlcPAOlnUx?from=from_copylink)

![img.png](docs/assets/img.png)

### 测试结果报告

![img_1.png](docs/assets/img_1.png)

### 异常接口超时记录[异常接口信息](https://vcn25s6jh1tk.feishu.cn/base/Bk4CbfXQ0adtvmsaSitcDoBrnyc?table=tbl0rIx1AqSP5Ns0&view=vewsx1D6PF)

![img_2.png](docs/assets/img_2.png)





