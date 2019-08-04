try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = '0.7.0'

with open('requirements.txt') as requirements_file:
    requires = [item for item in requirements_file]

with open('LICENSE') as f:
    license = f.read()

setup(
    name='pyWAMPBaseApp',
    version=version,
    description="Utility classes for creating WAMP enabled applications",
    long_description="",
    author='Cléber Zavadniak',
    author_email='contato@cleber.solutions',
    url='https://github.com/cleber-solutions/pyWAMPBaseApp',
    license=license,
    packages=['wampbaseapp'],
    package_data={'': ['AUTHORS.md', 'README.md']},
    include_package_data=True,
    install_requires=requires,
    zip_safe=False,
    keywords='generic libraries',
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ),
)
