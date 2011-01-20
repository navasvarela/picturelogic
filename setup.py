#!/usr/bin/env python

from distutils.core import setup 

setup(name='PictureLogic',
      version='1.0',
      description='Picture management and database program',
      author='Juan M Salamanca',
      author_email='juan.m.salamanca@gmail.com',
      url='http://www.salatecsolutions.com/picturelogic',
      package_data={'': ['logging.conf'],'db': ['structure.sql'], 'gui':['gui.glade']},
      packages=['','core','gui','db'],
     )
