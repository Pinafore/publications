#!/usr/bin/python

"""Splits an input pdf file into several given a list of splitting
points (page numbers).
"""

__author__ = 'benhdj@cs.cmu.edu (Benjamin Han)'


import sys
import os
from PyPDF2 import PdfFileReader, PdfFileWriter


def Usage ():
  print("""
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

  """)

def pdf_splitter(source, splits, target):
    pdf = PdfFileReader(source)
    num_pages = pdf.getNumPages()

    last_page = 0
    for ii in splits:
        pdf_writer = PdfFileWriter()
        output_filename = '{}_page_{}.pdf'.format(target, last_page)
        with open(output_filename, 'wb') as out:
          for jj in range(last_page, ii):
            pdf_writer.addPage(pdf.getPage(jj))
          pdf_writer.write(out)
        last_page = ii
        print('Created: {}'.format(output_filename))
  
if __name__ == "__main__":
  if len(sys.argv) < 3:
    Usage()
    sys.exit(1)
  else:
    inputFN = sys.argv[1]

  if inputFN:
    pdf = PdfFileReader(inputFN)
    maxPages = pdf.getNumPages()    
    print('%s has %d pages' % (inputFN, maxPages))
  else:
    sys.exit(2)

  try:
    splitPageNums = list(map(int,  sys.argv[2:]))
  except:
    print('Error: invalid split page number(s).')

  splitPageNums.append(maxPages)
  print("Got splits %s" % str(splitPageNums))

  pdf_splitter(inputFN, splitPageNums, inputFN.split(".")[0])
    
