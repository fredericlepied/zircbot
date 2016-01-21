from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='zircbot',
    version='0.0.1',
    description='An IRC bot that retrieve message from 0MQ',
    long_description=long_description,

    url='https://github.com/fredericlepied/zircbot',

    author='Frederic Lepied',
    author_email='flepied@redhat.com',

    license='Apache v2.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    keywords='irc bot 0mq',

    packages=find_packages(exclude=['tests']),

    install_requires=['txzmq', 'PyYAML'],

    entry_points={
        'console_scripts': [
            'zircbot=zircbot:main',
        ],
    },
)
