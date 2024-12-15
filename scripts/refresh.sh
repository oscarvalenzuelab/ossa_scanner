#!/bin/bash
rm -rf dist/* build/*
python3 setup.py sdist bdist_wheel > scripts/build.log
pip3 uninstall ossa_scanner > scripts/install.log
rm -rf /opt/homebrew/lib/python3.12/site-packages/ossa_scanner/ >> scripts/install.log
pip3 install dist/ossa_scanner-*-py3-none-any.whl --force-reinstall --no-deps >> scripts/install.log