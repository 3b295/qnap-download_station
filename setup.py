# coding:utf-8

from setuptools import setup

setup(
        name='qnap-download_station',
        version='1.0',
        description='an unofficial client for the QNAP api,',
        author='3b295',
        author_email='xwystz@gmail.com',
        packages=['qnap_downloadstation'],
)

install_requires=[
    'requests>=2.0',
]
