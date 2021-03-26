from setuptools import setup

setup(
    name='django-agnocomplete',
    version='1.1.0.dev0',
    packages=['agnocomplete'],
    include_package_data=True,
    description='Frontend-agnostic Django autocomplete utilities',
    url="https://github.com/peopledoc/django-agnocomplete",
    author='PeopleDoc Inc.',
    license='MIT',
    install_requires=[
        'Django>=2.2,<3.0',
        'six',
        'requests',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
