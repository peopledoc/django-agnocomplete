from setuptools import setup

setup(
    name='django-agnocomplete',
    version='0.13.0.dev0',
    packages=['agnocomplete'],
    include_package_data=True,
    description='Frontend-agnostic Django autocomplete utilities',
    url="https://github.com/peopledoc/django-agnocomplete",
    author='PeopleDoc Inc.',
    license='MIT',
    install_requires=[
        'Django',
        'six',
        'requests',
    ],
)
