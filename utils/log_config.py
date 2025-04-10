import os
from datetime import datetime
from loguru import logger

def setup_logger():
    """配置日志记录器
    
    设置日志文件名格式为：logs/test_YYYY-MM-DD_HH-mm-ss.log
    配置日志记录格式，包含时间、日志级别、文件名、行号和消息
    """
    # 确保logs目录存在
    log_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # 生成带时间戳的日志文件名
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_file = os.path.join(log_dir, f'test_{timestamp}.log')
    
    # 移除默认的日志处理器
    logger.remove()
    
    # 添加新的日志处理器
    logger.add(
        log_file,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {file}:{line} | {message}",
        level="INFO",
        rotation=None,  # 禁用日志轮转，每次运行生成新文件
        encoding='utf-8'
    )
    
    return logger