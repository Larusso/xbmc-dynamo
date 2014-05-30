from distutils.core import setup

setup(
    name='XBMC-Dynamo',
    version='0.1.0',
    author='M. Endres',
    packages=['xbmcdynamo'],
    scripts=['xbmcdynamo/bin/dynamo.py'],
    entry_points={'console_scripts': [
        'xbmc-dynamo = xbmcdynamo:execute_from_command_line',
    ]},
    url='http://pypi.python.org/pypi/XBMC-Dynamo/',
    license='LICENSE.txt',
    description='XBMC repository generator and publisher',
    long_description=open('README.txt').read(),
    install_requires=[
        'sh'=='1.09',
    ],
)