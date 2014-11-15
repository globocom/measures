from setuptools import setup, find_packages


README = open('README.md').read()


setup(name="Measure",
      author="Globo.com",
      author_email="busca@corp.globo.com",
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python'],
      download_url = '',
      description=u"Library for posting metrics to a server",
      include_package_data=True,
      install_requires=[],
      license="MIT",
      long_description=README,
      packages=find_packages(),
      tests_require=["coverage==3.6", "nose==1.2.1", "pep8==1.4.1", "mock==1.0.1", "pylint==1.0.0"],
      url = "http://github.com/globocom/measure",
      version="1.0.0"
)
