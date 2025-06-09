from setuptools import setup

setup(
    name='anatra',
    version='0.1',
    py_modules=['anatra'],
    entry_points={
        'console_scripts': [
            'anatra = anatra:main',
        ],
    },
    install_requires=[
        'platformdirs',
        # other dependencies...
    ],
)

