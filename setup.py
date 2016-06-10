try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Apertura genetic data pre-processing framework.',
    'author': 'Dillon Graham',
    'url': 'https://github.com/dgraham66/apertura_dev',
    'download_url': 'https://github.com/dgraham66/apertura_dev.git',
    'author_email': 'dgraham24@unm.edu',
    'version': '0.1',
    'install_requires': ['nose','django'],
    'packages': ['APERTURA','apertura_gui'],
    'plink_scripts': [],
    'name': 'apertura'
}

setup(**config)