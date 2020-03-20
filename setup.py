from distutils.core import setup


with open('README') as f:
    README = f.read()


setup(name="measures",
      version="1.4.0",
      description=u"Library for posting metrics to a server",
      long_description=README,
      author="Globo.com",
      author_email="busca@corp.globo.com",
      url="http://github.com/globocom/measures",
      download_url='',
      license="MIT",
      packages=[''],
      package_dir={'': 'src'},
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Programming Language :: Python'
      ],
      include_package_data=True,
      zip_safe=True,
      install_requires=[],
      tests_require=["coverage==3.6", "nose==1.2.1", "pep8==1.4.1", "mock==1.0.1", "pylint==1.0.0"],
)
