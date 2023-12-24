from setuptools import setup, find_packages

# 读取README.md的内容作为long_description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fast_script_utils",
    version="0.0.1",
    packages=find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[],  # 依赖列表，格式是 ['package>=version']
)
