from setuptools import setup, find_packages

setup(
    name='manage-sql',
    version='0.4.2',
    author='Web Tech Moz',
    author_email='zoidycine@gmail.com',
    description='Biblioteca Python para gestão de bases de dados SQLite e MYSQL com maior eficiência',
    long_description=open('README.md', 'r', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/webtechmoz/manage-sql',
    packages=find_packages(),
    keywords=['manage-sql', 'sqlite', 'sqlite manager', 'mysql', 'mysql manager', 'mysql python', 'mysql connector'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "deprecated",
        "dataclasses",
        "mysql-connector",
        "mysql-connector-python",
        "pandas"
    ],
    python_requires='>=3.10',
)