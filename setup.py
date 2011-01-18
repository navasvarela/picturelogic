#!/usr/bin/env python

from cx_Freeze import setup, Executable

includes = ['cairo','pangocairo']

target_1 = Executable(
       # what to build
       script = "picturelogic.py",
       initScript = None,
       targetDir = r"dist/linux",
       targetName = "picturelogic",
       compress = True,
       copyDependentFiles = True,
       appendScriptToExe = False,
       appendScriptToLibrary = False,
       icon = None
       )

setup(name='Picturelogic',
      version='1.0',
      description='Picture management and database program',
      author='Juan M Salamanca',
      author_email='juan.m.salamanca@gmail.com',
      url='http://www.salatecsolutions.com/picturelogic',
      options = { "build_exe": {"includes": includes}
		},
      executables = [target_1]
     )
