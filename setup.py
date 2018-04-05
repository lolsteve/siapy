try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup

from sia import __version__, __authors__, __emails__


setup(
    name='essentia-sia-api',
    version=__version__,
    author=__authors__,
    author_email=__emails__,
    url='https://github.com/essentiaone/essentia-sia-api',
    description='Sia API wrapper written in Python.',
    download_url='https://github.com/essentiaone/essentia-sia-api/archive/master.zip',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests>=2.18.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ]
)
