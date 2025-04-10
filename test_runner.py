import os
import pytest
from typing import Dict, Any
from utils.http_client import HTTPClient
from utils.test_loader import TestLoader
from loguru import logger

def run_test_case(http_client: HTTPClient, test_case: Dict[str, Any]) -> bool:
    """执行单个测试用例"""
    try:
        # 发送请求
        request_data = test_case['request']
        method = request_data['method']
        url = request_data['url']
        kwargs = {k: v for k, v in request_data.items() if k not in ['method', 'url']}
        
        response = http_client.request(method, url, **kwargs)

        # 提取数据
        if 'extract' in test_case:
            for var_name, extract_expr in test_case['extract'].items():
                value = http_client.extract_data(response, extract_expr)
                if value is not None:
                    http_client.set_variable(var_name, value)
                else:
                    logger.error(f"Failed to extract {var_name} using {extract_expr}")
                    return False

        # 验证响应
        if 'validate' in test_case:
            expected = test_case['validate'].copy()
            if 'status_code' in expected:
                if response.status_code != expected.pop('status_code'):
                    logger.error(f"Status code validation failed: expected {expected['status_code']}, got {response.status_code}")
                    return False
            
            if not http_client.validate_response(response, expected):
                return False

        return True

    except Exception as e:
        logger.error(f"Test case execution failed: {e}")
        return False

def pytest_generate_tests(metafunc):
    """动态生成测试用例"""
    if 'test_case' in metafunc.fixturenames:
        test_dir = os.path.join(os.path.dirname(__file__), 'testcases')
        test_files = TestLoader.get_test_files(test_dir)
        test_cases = []
        
        for test_file in test_files:
            cases = TestLoader.load_test_cases(test_file)
            test_cases.extend(cases)
        
        metafunc.parametrize('test_case', test_cases, ids=[case.get('name', f'test_{i}') for i, case in enumerate(test_cases)])

@pytest.fixture(scope='session')
def http_client(env_config):
    """创建HTTP客户端实例"""
    env = os.getenv('TEST_ENV', 'dev')
    config = env_config[env]
    client = HTTPClient(config['base_url'])
    client.session.headers.update(config.get('headers', {}))
    client.session.timeout = config.get('timeout', 30)
    return client

def test_api(http_client, test_case):
    """测试用例执行入口"""
    assert run_test_case(http_client, test_case), f"Test case '{test_case.get('name', 'Unknown')}' failed"