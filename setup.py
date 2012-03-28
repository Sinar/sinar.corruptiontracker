from setuptools import setup, find_packages
import sys,os

version = '0.1'

setup(name='sinar.corruptiontracker',
      version=version,
      description="Sinar Corruption Tracker Application",
      long_description="""
      """,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='',
      author='Khairil Yusof',
      author_email='khairil.yusof@gmail.com',
      url='https://github.com/Sinar/sinar.corruptiontracker',
      license='GPL',
      packages=find_packages('src',exclude=['ez_setup']),
      namespace_packages=['sinar'],
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Plone',
          'plone.app.dexterity',
          'collective.autopermission',
          'collective.portlet.collectionmultiview',
          # -*- Extra requirements: -*-
          'ipdb',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
