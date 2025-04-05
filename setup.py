from setuptools import setup, find_packages

setup(
    name='crew_automation_for_shopify_e_commerce_integration',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'flask>=2.0.1',
        'shopify>=12.1.0',
        'instagram-private-api>=1.6.0.0',
        'python-dotenv>=0.19.0',
        'Werkzeug>=2.0.1',
        'Jinja2>=3.0.1',
        'MarkupSafe>=2.0.1',
        'itsdangerous>=2.0.1',
        'click>=8.0.1',
        'requests>=2.26.0',
        'urllib3>=1.26.6',
        'certifi>=2021.5.30',
        'chardet>=4.0.0',
        'idna>=3.2'
    ],
    python_requires='>=3.8'
)