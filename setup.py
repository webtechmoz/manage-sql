from setuptools import setup, find_packages

setup(
    name='manage-sql',
    version='0.5.0',
    author='Web Tech Moz',
    author_email='zoidycine@gmail.com',
    description='Biblioteca Python para gestão de bases de dados SQLite, MYSQL e PostgreSQL com maior eficiência',
    long_description=open('README.md', 'r', encoding='UTF-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/webtechmoz/manage-sql.git',
    packages=find_packages(),
    keywords=['manage-sql', 'sqlite', 'sqlite manager', 'mysql', 'mysql manager', 'mysql python', 'mysql connector', 'postgresql connector', 'postgresql', 'postgresql python'],
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "dataclasses",
        "mysql-connector",
        "mysql-connector-python",
        "pandas",
        "psycopg2-binary"
    ],
    python_requires='>=3.10',
)