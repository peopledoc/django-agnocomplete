from setuptools import setup

setup(
    name='django-agnocomplete',
    version='0.0.0',
    packages=['agnocomplete'],
    include_package_data=True,
    description='Frontend-agnostic Django autocomplete utilities',
    author='Novapost',
    install_requires=[
        'Django',
    ],
)
