# 使用Python 3.12基础镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1

# 复制项目文件
COPY . /app/

# 安装项目依赖
RUN pip install --no-cache-dir -r requirements.txt

# 设置默认命令
CMD ["pytest"]