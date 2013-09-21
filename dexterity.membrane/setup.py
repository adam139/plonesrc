from setuptools import setup, find_packages

version = '0.3.dev0'

setup(name='dexterity.membrane',
      version=version,
      description="Dexterity content and behaviors to integrate with membrane.",
      long_description=(open("README.txt").read() + "\n" +
                        open("CHANGES.rst").read()),
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          "Framework :: Plone",
          "Programming Language :: Python",
          ],
      keywords='',
      author='Maurits van Rees',
      author_email='maurits@vanrees.org',
      url='https://github.com/collective/dexterity.membrane',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['dexterity'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone>=4.1b1',
          'plone.app.dexterity',
          'Products.membrane>=2.0.2',
          'collective.indexing',
          'plone.formwidget.captcha',
          'collective.monkeypatcher',          
          'plone.app.referenceablebehavior',
          'incf.countryutils',
      ],
       extras_require={
          'test': ['plone.app.testing',]
          },         
      entry_points="""
      # -*- Entry points: -*-

      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
