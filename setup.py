from setuptools import setup, find_packages
import os

version = '0.3.dev0'

setup(name='plone.z3ctable',
      version=version,
      description="z3c.table support for Plone",
      long_description=open("README.txt").read() + "\n" +
      open(os.path.join("docs", "HISTORY.txt")).read(),
      classifiers=[
          'Programming Language :: Python',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Framework :: Plone :: 4.3',
          'Framework :: Plone :: 5.0',
          'Framework :: Plone :: 5.1',
          'Framework :: Plone :: 5.2',
      ],
      keywords='',
      author='Godefroid Chapelle',
      author_email='gotcha@bubblenet.be',
      url='https://github.com/affinitic/plone.z3ctable',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['plone'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'z3c.table',
          'Zope2',
          'Products.CMFPlone',
          'zope.i18n',
          # -*- Extra requirements: -*-
      ],
      extras_require={'test': [
          'z3c.table [test]',
      ]},
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
