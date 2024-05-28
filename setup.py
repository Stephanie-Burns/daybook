from setuptools import setup, find_packages

setup(
    name='daybook',
    version='1.0.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        'cryptography>=3.4.7',
    ],
    entry_points={
        'console_scripts': [
            'daybook=daybook.daybook:main',
        ],
    },
    author='Stephanie Burns',
    author_email='stephanieburns404@gmail.com',
    description='A command-line tool for managing daily journal entries with encryption.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Stephanie-Burns/daybook',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
