from setuptools import setup
from setuptools.command.install import install
import subprocess
from os.path import join, dirname


class CompileParser(install):
    def run(self):
        install.run(self)
        import stanford_parser
        pwd = stanford_parser.__path__[0]
        print 'install path', pwd

        subprocess.Popen(['wget', 'https://github.com/banyh/StanfordParserServer/archive/PyStanfordParser.zip'], cwd=pwd)
        subprocess.Popen(['unzip', '-o', '-j', 'PyStanfordParser.zip'], cwd=pwd)
        subprocess.Popen(['install.sh'], cwd=pwd)


setup(name='PyStanfordParser',
      version='0.1.0',
      description='Wrapping Stanford parser as a python package',
      url='https://github.com/banyh/PyStanfordParser',
      author='Ping Chu Hung',
      author_email='banyhong@gliacloud.com',
      license='MIT',
      packages=['stanford_parser'],
      zip_safe=False,
      install_requires=[
          'numpy',
          'jpype1',
      ],
      cmdclass={
          'install': CompileParser,
      },
      test_suite='nose.collector',
      tests_require=['nose'],
      include_package_data=True,)
