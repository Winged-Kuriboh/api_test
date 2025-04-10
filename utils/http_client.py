import requests
from typing import Dict, Any
from jsonpath import jsonpath
from loguru import logger

class HTTPClient:
    def __init__(self, base_url: str = ''):
        self.base_url = base_url
        self.session = requests.Session()
        self._variables = {}

    def set_variable(self, name: str, value: Any) -> None:
        """设置变量，用于接口关联"""
        self._variables[name] = value

    def get_variable(self, name: str) -> Any:
        """获取变量值"""
        return self._variables.get(name)

    def _handle_parameters(self, data: Dict) -> Dict:
        """处理参数中的变量引用，支持 ${variable} 格式"""
        if not data:
            return data

        processed_data = {}
        for key, value in data.items():
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                var_name = value[2:-1]
                processed_data[key] = self.get_variable(var_name)
            else:
                processed_data[key] = value
        return processed_data

    def request(self, method: str, url: str, **kwargs) -> requests.Response:
        """发送HTTP请求"""
        full_url = f"{self.base_url}{url}" if self.base_url else url
        
        # 处理请求参数中的变量
        if 'json' in kwargs:
            kwargs['json'] = self._handle_parameters(kwargs['json'])
        if 'params' in kwargs:
            kwargs['params'] = self._handle_parameters(kwargs['params'])

        logger.info(f"Sending {method} request to {full_url}")
        logger.info(f"Request parameters: {kwargs}")

        response = self.session.request(method, full_url, **kwargs)
        logger.info(f"Response status code: {response.status_code}")
        logger.info(f"Response body: {response.text}")

        return response

    def extract_data(self, response: requests.Response, extract_expr: str) -> Any:
        """使用JSONPath从响应中提取数据"""
        try:
            json_data = response.json()
            result = jsonpath(json_data, extract_expr)
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Failed to extract data: {e}")
            return None

    def validate_response(self, response: requests.Response, expected: Dict) -> bool:
        """验证响应结果"""
        try:
            json_data = response.json()
            for key, value in expected.items():
                if isinstance(value, str) and value.startswith('$'):
                    actual = jsonpath(json_data, value)
                    if not actual:
                        logger.error(f"Validation failed: {key} not found in response")
                        return False
                    actual = actual[0]
                else:
                    actual = json_data.get(key)
                
                if actual != value:
                    logger.error(f"Validation failed: expected {key}={value}, got {actual}")
                    return False
            return True
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return False