# Usage:
# in the base pinafore papers directory:
# > ./scripts/camera_copy.sh 20XX_CONF_PAPER ~/repositories/publications
# If the directories aren't the same, you might break stuff

# clean up cruft
make clean

# Copy any of the shared files
cp Makefile $2

for DIR in scripts bib style
do
    # rm -r $DIR
    # git checkout $DIR
    mkdir -p $2/$DIR
    echo cp $DIR/*.* $2/$DIR
    cp $DIR/*.* $2/$DIR
    echo $DIR done
done



echo "------------"
mkdir -p $2/$1
cp $1.tex $2/$1.tex
if [ -s $1/figures.R ]
then
    cp $1/figures.R $2/$1
fi
if [ -s $1/figures.py ]
then
    cp $1/figures.py $2/$1
fi

for DIR in figures sections data tables
do
    # rm -r $1/$DIR
    # git checkout $1/$DIR
    mkdir -p $2/$1/$DIR
    cp $1/$DIR/*.* $2/$1/$DIR
done

echo "------------"
cd $2
python scripts/sanitize.py $1/sections
echo "------------"
git add Makefile scripts/*
git add `python scripts/latex_deps.py $1.tex`
git add $1/figures/*.* $1/sections/*.* $1/data/*.* $1.tex
if [ -s $1/figures.R ]
then
   git add $1/figures.R
fi
git commit -m "Import of $1" -a
