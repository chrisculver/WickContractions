# Readme

This code computes the wick contractions for LQCD operators that contain
quark fields.  The final result is a list of diagrams that are to be 
evaluated numerically to obtain the correlation function.

## Installation

Install locally in a conda environment with `pip install -e .`

## Examples

For the charged pion check out PionCorrelator.ipynb.

## Tests and Code Coverage

To run all the tests type
    coverage run -m pytest
Then
    coverage report -m  
To make this work I have added an empty conftest.py to WickContractions, to trick pytest.

## Docs

CURRENTLY BROKEN
To create the docs type 'make html' or 'make latex' in the top directory.
If you make latex then go into docs/latex and type make again to generate the pdf.
If you make html then run firefox /docs/html/index.html.  This is the version
that will be uploaded to ReadTheDocs.
