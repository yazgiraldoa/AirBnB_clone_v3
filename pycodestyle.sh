#!/bin/bash
echo "------------Checking Root folder------------"
pycodestyle *.py
echo

echo "------------Checking into API folder------------"
pycodestyle api/*.py api/v1/*.py api/v1/views/*.py
echo

echo "------------Checking into MODELS folder------------"
pycodestyle models/*.py models/engine/*.py
echo

echo "------------Checking into TESTS folder------------"
pycodestyle tests/*.py tests/test_models/*.py tests/test_models/test_engine/*.py
echo

echo "------------Checking into WEB_FLASK folder------------"
pycodestyle web_flask/*.py
echo