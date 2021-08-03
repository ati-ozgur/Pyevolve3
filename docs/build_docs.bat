@echo off

rd /s/q build_htmlhelp
rd /s/q build_web
rd /s/q build_latex

sphinx-build -E -a -b htmlhelp .\source .\build_htmlhelp
sphinx-build -E -a -b html .\source .\build_web
sphinx-build -E -a -b latex .\source .\build_latex