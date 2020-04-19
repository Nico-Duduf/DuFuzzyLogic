#!/bin/sh
mkdocs build
echo "dufuzzylogic-docs.rainboxlab.org" > ../docs/CNAME
jsdoc -c jsdoc_Fuzzy.json
cp -f ../docs/js/FuzzyLogic.html ../docs/js/index.html
