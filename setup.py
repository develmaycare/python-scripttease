# See https://packaging.python.org/en/latest/distributing.html
# and https://docs.python.org/2/distutils/setupscript.html
# and https://pypi.python.org/pypi?%3Aaction=list_classifiers
from setuptools import setup, find_packages


def read_file(path):
    with open(path, "r") as f:
        contents = f.read()
        f.close()
    return contents


setup(
    name='python-script-tease',
    version=read_file("VERSION.txt"),
    description=read_file("DESCRIPTION.txt"),
    long_description=read_file("README.markdown"),
    author='Shawn Davis',
    author_email='shawn@myninjas.net',
    url='https://bitbucket.com/myninjas/python-script-tease',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "jinja2",
        "pygments",
        "python-myninjas",
    ],
    dependency_links=[
        "https://bitbucket.com/myninjas/python-myninjas/master.tar.gz#python-myninjas",
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    zip_safe=False,
    tests_require=[
        "coverage",
    ],
    test_suite='runtests.runtests',
    entry_points={
      'console_scripts': [
          'tease = script_tease.cli:main_command',
      ],
    },
)
