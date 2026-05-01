"""EquipMind AI 安装配置"""
from setuptools import setup, find_packages

with open("README.md", "w", encoding="utf-8") as f:
    f.write("# EquipMind AI\n\nAI驱动的IT基础设施智能监控预测系统")

setup(
    name="equipmind",
    version="1.0.0",
    description="EquipMind AI - AI驱动的IT基础设施智能监控预测系统",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.0",
        "rich>=13.0",
        "scikit-learn>=1.3",
        "pandas>=2.0",
        "numpy>=1.24",
        "matplotlib>=3.7",
    ],
    extras_require={
        "api": ["flask>=3.0"],
    },
    entry_points={
        "console_scripts": [
            "equipmind=equipmind.cli.main:cli",
        ],
    },
    python_requires=">=3.10",
)
