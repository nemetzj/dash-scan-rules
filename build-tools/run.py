#!/usr/bin/python3

#Python runner file
from artifacts import *
from rulesets_build import *


artifacts = artifact_set()
artifacts.createDirs()

build_all_rulesets()