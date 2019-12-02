from setuptools import setup
import sys,os

with open('pybioviz/description.txt') as f:
    long_description = f.read()

setup(
    name = 'pybioviz',
    version = '0.1.0',
    description = 'bioinformatic dashboards with panel/bokeh',
    long_description = long_description,
    url='https://github.com/dmnfarrell/pybioviz',
    license='GPL v3',
    author = 'Damien Farrell',
    author_email = 'farrell.damien@gmail.com',
    packages = ['pybioviz'],
    package_data={'pybioviz': ['data/*.*',
                  'notebooks/*.ipynb',
                  'templates/*.html',
                  'description.txt']
                 },
    install_requires=['numpy>=1.10',
                      'pandas>=0.24',
                      'biopython>=1.5',
                      'panel>=0.7.0',
                      'bokeh>=1.4',
                      'pyfaidx>0.5',
                      'pysam>0.15',
                      'bcbio_gff',
                      'future'],
    entry_points = {
        'console_scripts': [
            'pybioviz=pybioviz.app:main']
            },
    classifiers = ['Operating System :: OS Independent',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3.6',
            'Operating System :: MacOS :: MacOS X',
            'Operating System :: Microsoft :: Windows',
            'Operating System :: POSIX',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Development Status :: 4 - Beta',
            'Intended Audience :: Science/Research',
            'Topic :: Scientific/Engineering :: Bio-Informatics'],
    keywords = ['bioinformatics','biology','genomics','dashboard']
)
