import os
import pytest
from sqlalchemy import false
import yaml
from loguru import logger
from typing import Dict, Any
from app import app, db, User

def pytest_collection_modifyitems(items):
    for item in items:
        item.name = item.name.encode('utf-8').decode('unicode-escape')
        item._nodeid = item.nodeid.encode('utf-8').decode('unicode-escape')

@pytest.fixture(scope='session')
def env_config() -> Dict[str, Any]:
    """加载环境配置"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'env.yaml')
    with open(config_path, encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(scope='session')
def api_config() -> Dict[str, Any]:
    """加载API配置"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'api.yaml')
    with open(config_path, encoding='utf-8') as f:
        return yaml.safe_load(f)

@pytest.fixture(autouse=True)
def setup_logging():
    """配置日志"""
    from utils.log_config import setup_logger
    return setup_logger()

@pytest.fixture(autouse=False)
def setup_database():
    """初始化数据库"""
    with app.app_context():
        db.drop_all()
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()