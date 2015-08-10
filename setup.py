#!/usr/bin/env python

from distutils.core import setup

setup(name="sbd",
      version="0.1",
      description="Iridium Short Burst Data DirectIP handling",
      author="Pete Gadomski",
      author_email="pete.gadomski@gmail.com",
      url="https://github.com/gadomski/sbd",
      packages=["sbd"],
      scripts=["bin/iridiumd"],
      install_requires=[
          "python-daemon",
          ]
      )
