from setuptools import setup

setup(
    name='django-agnocomplete',
    version='0.4rc1',
    packages=['agnocomplete'],
    include_package_data=True,
    description='Frontend-agnostic Django autocomplete utilities',
    author='Novapost',
    license='MIT',
    install_requires=[
        'Django',
        'six'
    ],
)
