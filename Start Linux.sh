#!/bin/sh

set "PYTHON="
set "VENV_DIR="
set "COMMANDLINE_ARGS="

if [ -z "$PYTHON" ]
then
      PYTHON=python3
fi

if [ -z "$VENV_DIR" ]
then
      VENV_DIR="${0%/*}/venv"
fi

if [ ! -f "${VENV_DIR}/bin/activate" ]
then
      echo Creating virtual environment
      $PYTHON -m venv "${VENV_DIR}"
      echo
fi


echo Attempting to start venv
. "${VENV_DIR}/bin/activate"
echo

echo Updating Pip
$PYTHON -m pip install --upgrade pip
echo

echo Installing required packages
pip install -r requirements.txt
echo

clear
python3 main.py