from setuptools import setup
from setuptools.command.install import install
import subprocess
from os.path import join, dirname, isfile
import sys
import time


class CompileParser(install):
    def run(self):
        install.run(self)
        sys.path.reverse()
        import stanford_parser
        pwd = stanford_parser.__path__[0]

        subprocess.Popen(['wget', 'https://github.com/banyh/StanfordParserServer/archive/PyStanfordParser.zip'], cwd=pwd)
        while not isfile(join(pwd, 'PyStanfordParser.zip')):
            time.sleep(0.1)
        subprocess.Popen(['unzip', '-o', '-j', 'PyStanfordParser.zip'], cwd=pwd)
        while not isfile(join(pwd, 'install.sh')):
            time.sleep(0.1)
        subprocess.Popen(['./install.sh'], cwd=pwd, shell=True)


setup(name='PyStanfordParser',
      version='0.2.0',
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
