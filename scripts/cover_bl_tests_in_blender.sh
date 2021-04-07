#!/bin/sh
${BLENDERPIP} install --no-cache-dir coverage
blender -b -P scripts/run_bl_tests_in_blender.py