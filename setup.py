from setuptools import setup, find_packages
import os

version = open(os.path.join("sc", "social", "bookmarks", "version.txt")).read().strip()
longdesc = open(os.path.join(os.path.dirname(__file__), 'README.txt')).read()
longdesc += open(os.path.join(os.path.dirname(__file__), 'docs', 'HISTORY.txt')).read()

setup(name='sc.social.bookmarks',
      version=version,
      description="Add social bookmarking and sharing capabilities to a Plone Site",
      long_description=longdesc,
      # Get more strings from http://www.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone web social bookmarks delicious digg',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['sc', 'sc.social'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # I don't understand why, but if I don't include this package I get "ImportError: No module named i18nmessageid"
          'Plone',
          # same thing, I get "ImportError: No module named PIL"
          'PIL',
#          'plone.app.registry',
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
