import unittest

from src.time import parse_time_to_ms


class MyTestCase(unittest.TestCase):
    def test_parse_time(self):
        # 测试函数
        test_cases = [
            "100s",
            "10min",
            "2h",
            "1.5d",
            "500ms",
            "1 hour",
            "2 days",
            "30",
            "45sec",
        ]

        for case in test_cases:
            try:
                result = parse_time_to_ms(case)
                print(f"{case} = {result} ms")
            except ValueError as e:
                print(f"Error parsing {case}: {str(e)}")


if __name__ == "__main__":
    unittest.main()
