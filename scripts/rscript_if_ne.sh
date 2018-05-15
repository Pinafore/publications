#!/bin/bash -e

if hash python3 2>/dev/null; then
        PYCOMMAND=python3
else
        PYCOMMAND=python
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
