import os
import yaml
from typing import Dict, List, Any
from loguru import logger

class TestLoader:
    @staticmethod
    def load_test_cases(test_file: str) -> List[Dict[str, Any]]:
        """从YAML文件加载测试用例"""
        try:
            with open(test_file, encoding='utf-8') as f:
                test_cases = yaml.safe_load(f)
            return TestLoader._process_test_cases(test_cases)
        except Exception as e:
            logger.error(f"Failed to load test cases from {test_file}: {e}")
            return []

    @staticmethod
    def _process_test_cases(test_cases: List[Dict]) -> List[Dict[str, Any]]:
        """处理测试用例，支持数据驱动和接口关联"""
        processed_cases = []
        for case in test_cases:
            # 处理数据驱动
            if 'parametrize' in case:
                processed_cases.extend(
                    TestLoader._handle_parametrize(case)
                )
            else:
                processed_cases.append(case)
        return processed_cases

    @staticmethod
    def _handle_parametrize(case: Dict) -> List[Dict]:
        """处理参数化测试数据"""
        param_cases = []
        params = case['parametrize']
        template = {k: v for k, v in case.items() if k != 'parametrize'}

        for param_set in params:
            new_case = template.copy()
            # 更新请求数据
            if 'request' in new_case and 'json' in new_case['request']:
                new_case['request']['json'].update(param_set)
            elif 'request' in new_case:
                new_case['request']['json'] = param_set
            # 更新用例名称
            new_case['name'] = f"{new_case['name']}_{param_set}"
            param_cases.append(new_case)

        return param_cases

    @staticmethod
    def get_test_files(test_dir: str) -> List[str]:
        """获取指定目录下的所有测试用例文件"""
        test_files = []
        for root, _, files in os.walk(test_dir):
            for file in files:
                if file.endswith('.yaml') and 'test' in file.lower():
                    test_files.append(os.path.join(root, file))
        return test_files