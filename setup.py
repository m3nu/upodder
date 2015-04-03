import re
import ast
from setuptools import setup

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('upodder/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))


description = 'Command Line Podcast Downloader'


setup(
        name='upodder',
        author='"Stan Vitkovskiy, Manuel Riel"',
        author_email='stas.vitkovsky[at]gmail.com, manu[at]vlx.cc',
        version=version,
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
            'sqlobject'
            ],
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: End Users/Desktop',
            'License :: OSI Approved :: MIT License',
            'Operating System :: Unix',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: News/Diary',
            ],
        )
