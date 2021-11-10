# Readme

This code computes the wick contractions for LQCD operators that contain
quark fields.  The final result is a list of diagrams that are to be 
evaluated numerically to obtain the correlation function.


## Examples
Features of this code are being worked on in prototyping.nb, which includes a
simple SU(4) baryon-baryon scattering contraction with LapH.

Usage of this code without LapH can be seen in test_contractions.py, where SU(3)
pion and nucleon correlation functions are checked explicitly.

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
