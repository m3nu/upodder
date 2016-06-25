import re
import ast
from setuptools import setup

description = 'Command Line Podcast Downloader'

setup(
        name='upodder',
        author='"Stan Vitkovskiy, Manuel Riel"',
        author_email='stas.vitkovsky[at]gmail.com, manu[at]vlx.cc',
        version='0.6.3',
        license='LICENSE.txt',
        url='https://github.com/manuelRiel/upodder',
        description=description,
        packages=['upodder', 'upodder.test'],
        entry_points={'console_scripts': ['upodder = upodder.upodder:main']},
        long_description=open('README.rst').read(),
        install_requires=[
            'clint',
            'requests',
            'feedparser',
            'sqlobject >=3.0.0a2dev-20151224',
            ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
            ],
        )
