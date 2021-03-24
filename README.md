# Readme

This code computes the wick contractions for LQCD operators that contain
quark fields.  The final result is a list of diagrams, which can be computed
with any LQCD software stack.  

## Examples

The main usage of this code can be seen in test_contractions.py, where the
pion and nucleon correlation functions are checked explicitly.  Additional
functionality, for reducing the number of diagrams, can be found in 'blank'.

## Tests and Code Coverage
To run all the tests type 'coverage run -m pytest'.  Then 'coverage report -m'.  
To make this work I have added an empty conftest.py to src, to trick pytest.

## Docs
To create the docs type 'make html' or 'make latex' in the top directory.
If you make latex then go into docs/latex and type make again to generate the pdf.
If you make html then run firefox /docs/html/index.html.  This is the version
that will be uploaded to ReadTheDocs.
