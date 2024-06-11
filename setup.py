from setuptools import setup, find_packages

setup(
    name='AC_TELEMETRY',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'dash',
        'dash-bootstrap-components',
        'pyyaml',
    ],
    entry_points={
        'console_scripts': [
            'run-my-project=AC_TELEMETRY.app:main',
        ],
    },
)
