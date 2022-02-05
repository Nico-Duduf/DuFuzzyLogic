#!/bin/sh
mkdocs build
echo "dufuzzylogic.rxlab.io" > ../docs/CNAME
jsdoc -c jsdoc_Fuzzy.json
cp -f ../docs/js-reference/FuzzyLogic.html ../docs/js-reference/index.html
