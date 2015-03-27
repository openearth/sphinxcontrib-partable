from setuptools import setup, find_packages

setup(
    name='sphinxcontrib-partable',
    version='0.0',
    author='Bas Hoonhout',
    author_email='bas.hoonhout@deltares.nl',
    packages=find_packages(),
    description='Sphinx parameter table extension',
    long_description=open('README.txt').read(),
    install_requires=[],
    setup_requires=[
        'Sphinx',
    ],
    zip_safe=False,
    namespace_packages=['sphinxcontrib'],
)
