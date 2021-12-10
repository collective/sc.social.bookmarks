# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = "1.3dev"

long_description = "\n\n".join(
    [
        open("README.rst").read(),
        open("CONTRIBUTORS.rst").read(),
        open("CHANGES.rst").read(),
    ]
)

setup(
    name="sc.social.bookmarks",
    version=version,
    description="""Add social bookmarking and sharing capabilities to a
                     Plone Site""",
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Stable",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.2",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone web social bookmarks delicious digg",
    author="Simples Consultoria",
    author_email="products@simplesconsultoria.com.br",
    url="http://www.simplesconsultoria.com.br/",
    license="GPL",
    packages=find_packages("src"),
    package_dir={"": "src"},
    namespace_packages=["sc", "sc.social"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "Products.CMFCore",
        "Products.CMFPlone >=5.2",
        "plone.app.controlpanel",
        "plone.app.layout",
        "plone.app.portlets",
        "plone.app.registry",
        "plone.memoize",
        "plone.portlets",
        "plone.registry",
        "zope.app.form",
        "zope.component",
        "zope.formlib",
        "zope.i18nmessageid",
        "zope.interface",
        "zope.schema",
    ],
    extras_require={
        "develop": [
            "Sphinx",
            "manuel",
            "pep8",
            "setuptools-flakes",
        ],
        "test": ["interlude", "plone.app.testing"],
    },
    entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
)
