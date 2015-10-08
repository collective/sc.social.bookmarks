from setuptools import setup, find_packages
import os

version = '1.3.3.dev0'
long_description = (open("README.txt").read() + "\n" +
                    open(os.path.join("docs", "INSTALL.txt")).read() + "\n" +
                    open(os.path.join("docs", "CREDITS.txt")).read() + "\n" +
                    open(os.path.join("docs", "HISTORY.txt")).read())

setup(name='sc.social.bookmarks',
      version=version,
      description="""Add social bookmarking and sharing capabilities to a
                     Plone Site""",
      long_description=long_description,
      classifiers=[
          "Development Status :: 5 - Production/Stable",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.1",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: Developers",
          "Operating System :: OS Independent",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Software Development :: Libraries :: Python Modules"],
      keywords='plone web social bookmarks delicious digg',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br/',
      license='GPL',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc', 'sc.social'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFCore',
          'Products.CMFDefault',
          'Products.CMFPlone',
          'plone.app.controlpanel',
          'plone.app.layout',
          'plone.app.portlets',
          'plone.app.registry',
          'plone.memoize',
          'plone.portlets',
          'plone.registry',
          'zope.app.form',
          'zope.component',
          'zope.formlib',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'develop': [
              'Sphinx',
              'manuel',
              'pep8',
              'setuptools-flakes',
          ],
          'test': [
              'interlude',
              'plone.app.testing'
          ]
      },
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
