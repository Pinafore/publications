#!/usr/bin/python

"""Splits an input pdf file into several given a list of splitting
points (page numbers).
"""

__author__ = 'benhdj@cs.cmu.edu (Benjamin Han)'


import sys
import os

from CoreGraphics import *


def Usage ():
  print """
Usage: splitPDF.py inputFN splitPageNum1 splitPageNum2 ...

  - inputFN: the path to the input pdf file.
    
  - splitPageNum1, ...: each one is a positive integer; the numbers
    must not exceed the number of pages of the input file, and the
    entire sequence must be strictly increasing.

Example: splitPDF.py input.pdf 3 5

This will split file input.pdf into 3 files (assuming input.pdf is 10
pages long):

  - input.part1.1_3.pdf contains page 1-3;
  
  - input.part2.4_5.pdf contains page 4-5;
  
  - input.part3.6_10.pdf contains page 6-10.

  """


if len(sys.argv) < 3:
  Usage()
  sys.exit(1)
else:
  inputFN = sys.argv[1]
  inputDoc = \
    CGPDFDocumentCreateWithProvider(\
    CGDataProviderCreateWithFilename(inputFN))

  if inputDoc:
    maxPages = inputDoc.getNumberOfPages()
    print '%s has %d pages' % (inputFN, maxPages)
  else:
    sys.exit(2)

  try:
    splitPageNums = map(int,  sys.argv[2:])
  except:
    print 'Error: invalid split page number(s).'

  for i, splitPageNum in enumerate(splitPageNums):
    if splitPageNum < 1 or splitPageNum > maxPages:
      print 'Error: a split page number must be >= 1 and <= %d.' % \
            maxPages
      sys.exit(3)
    elif i and splitPageNums[i - 1] >= splitPageNum:
      print 'Error: split page numbers must be increasing.'
      sys.exit(4)
    
baseFN = os.path.splitext(os.path.basename(inputFN))[0]
pageRect = CGRectMake (0, 0, 612, 792)

if splitPageNums[-1] < maxPages:
  splitPageNums.append(maxPages)

startPageNum = 1
for i, splitPageNum in enumerate(splitPageNums):
  outputFN = '%s.part%d.%d_%d.pdf' % \
             (baseFN, i + 1, startPageNum, splitPageNum)
  writeContext = CGPDFContextCreateWithFilename(outputFN, pageRect)

  print 'Writing page %d-%d to %s...' % \
        (startPageNum, splitPageNum, outputFN)

  for pageNum in xrange(startPageNum, splitPageNum + 1):
    mediaBox = inputDoc.getMediaBox(pageNum)
    writeContext.beginPage(mediaBox)
    writeContext.drawPDFDocument(mediaBox, inputDoc, pageNum)
    writeContext.endPage()

  startPageNum = splitPageNum + 1

print 'Done: %d file(s) generated.' % len(splitPageNums)
