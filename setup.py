from setuptools import setup, find_packages

setup(
    name="llmtest",
    version="0.1",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'llmtest=llmtest.__main__:main',
        ]
    }
)