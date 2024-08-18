from setuptools import setup, find_packages

setup(
    name='manage-sql',
    version='0.5.5',
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
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        "mysql-connector",
        "mysql-connector-python",
        "psycopg2"
    ],
    python_requires='>=3.6',
)