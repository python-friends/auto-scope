from setuptools import setup, find_packages

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='auto-scope',
    url='https://github.com/python-friends/auto-scope',
    author='Wytamma Wirth & Eike Steinig',
    author_email='python.friends.py@gmail.com',
    packages=find_packages(),
    install_requires=['RPi.GPIO'],
    version='0.1',
    license='MIT',
    description='An open source whole slide scanner and automated cell discrimination and counting system'
)