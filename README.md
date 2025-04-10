# 接口自动化测试框架

这是一个基于Python和pytest的接口自动化测试框架，支持通过YAML文件管理测试用例，实现接口关联，并生成美观的测试报告。

## 特点

- 使用YAML文件管理测试用例，结构清晰，易于维护
- 支持接口关联，可提取响应数据用于后续请求
- 支持参数化测试，提高测试覆盖率
- 灵活的数据提取和验证机制
- 美观的HTML测试报告
- 详细的日志记录

## 目录结构

```
.
├── config/                 # 配置文件目录
│   └── env.yaml           # 环境配置文件
├── testcases/             # 测试用例目录
│   └── test_user_flow.yaml # 示例测试用例
├── utils/                 # 工具类目录
│   ├── http_client.py     # HTTP请求客户端
│   └── test_loader.py     # 测试用例加载器
├── logs/                  # 日志目录
├── conftest.py           # pytest配置文件
├── test_runner.py        # 测试用例执行器
├── requirements.txt      # 项目依赖
└── README.md            # 项目说明文档

```

## 安装依赖

```bash
#2选1
使用包管理工具 uv 
pip install -r requirements.txt
```

## 使用方法

1. 配置环境信息
   - 在 `config/env.yaml` 中配置不同环境的接口地址和请求头信息

2. 编写测试用例
   - 在 `testcases` 目录下创建YAML格式的测试用例文件
   - 参考 `test_user_flow.yaml` 的格式编写测试用例

3. 运行测试
   ```bash
   # 运行所有测试用例
   pytest

   # 生成HTML报告
   pytest --html=report.html

   # 指定环境运行
   TEST_ENV=test pytest
   ```

## 测试用例示例

```yaml
- name: "用户注册接口测试"
  request:
    method: POST
    url: "/api/users"
    json:
      username: "testuser"
      email: "test@example.com"
  extract:
    user_id: "$.id"
  validate:
    status_code: 200
    message: "User created successfully"
```

## 特性说明

1. 接口关联
   - 使用 `extract` 提取响应数据
   - 通过 `${变量名}` 在后续请求中引用

2. 参数化测试
   - 使用 `parametrize` 定义多组测试数据
   - 自动生成多个测试用例

3. 响应验证
   - 支持状态码验证
   - 支持JSON响应内容验证
   - 支持JSONPath表达式提取和验证

4. 日志记录
   - 自动记录请求和响应信息
   - 记录测试执行过程中的关键信息

## 注意事项

1. 确保YAML文件格式正确
2. 接口关联变量需要先提取后使用
3. 参数化数据要与接口参数匹配
4. 建议使用相对路径配置接口URL