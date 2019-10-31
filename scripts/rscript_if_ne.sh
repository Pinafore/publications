#!/bin/bash -e

PYCOMMAND=python
if hash pythonw 2>/dev/null; then
    VERSION=`pythonw -c 'import platform; major, minor, patch = platform.python_version_tuple(); print(major);'`
    if [ $VERSION -eq 3 ]; then
        PYCOMMAND=pythonw
    else
        if hash python3 2>/dev/null; then
           PYCOMMAND=python3
        fi
    fi
else
    if hash python3 2>/dev/null; then
        PYCOMMAND=python3
    else
        PYCOMMAND=python
    fi
fi

echo $1
echo `which $PYCOMMAND`

if [ -f $1/figures.R ]; then
        echo "Running R"
        Rscript $1/figures.R
else
        echo "No RScripts!"
fi

if [ -f $1/figures.py ]; then
        echo "Running $PYCOMMAND"
        $PYCOMMAND $1/figures.py
else
        echo "No Python scripts!"
fi
