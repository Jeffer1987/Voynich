#
# This file is: http://www.voynich.nu/data/000_README.txt
# Latest update: 04/11/2023
#

The files in this directory, and the subdirectory /beta , are 
related to a general reformating of transliteration files of the 
Voynich MS text.

A new format, called IVTFF (Intermediate Voynich Transliteration
File Format) has been defined, such that it can represent all
existing and publicly available transliteration files in their own 
representation alphabet, in a consistent manner. This format
is presently (and for the foreseeable future) at a stable version
2.0, which only differs from the previous format (1.7) in very minor
details. All (five) transliteration files in this format now
include paragraph start markers and Lisa Fagin Davis' hand 
identification in page variable $H, making use of text tags in one
folio. Currier's old hand ID's are now in variable $C.

For general information see:
http://www.voynich.nu/transcr.html

For more specific information see:
http://www.voynich.nu/extra/transcr_new.html

Reasonably stable files are in the present directory.
Files that are still subject to change, and are being beta-tested,
may be found in subdirectory /beta , which also has its own
README file.

Two tools called "bitrans" and "ivtt" are able to read and process all 
files in this format. For these tools see:
http://www.voynich.nu/software/


--------------------------
Contents of this directory
--------------------------

CD2a-n.txt
----------
The conversion of the original Currier-D'Imperio transliteration into 
the IVTFF 2.0 format.
The file uses the Currier transliteration alphabet.
(The part of the file name saying "-n" refers to the native alphabet).


FG2a-n.txt
----------
The original FSG transliteration, in IVTFF 2.0 format.
The file uses the FSG transcription alphabet.


GC2a-n.txt
----------
A version of GC's v101 transliteration file in the IVTFF 2.0 format.
This file uses the v101 alphabet. Locus definition and ordering has
been changed (significantly!) such that it is now according to the 
IVTFF convention.


IT2a-n.txt
----------
The transliteration by Takeshi Takahashi, as included in the interlinear 
file by Jorge Stolfi in 1999, in the IVTFF 2.0 format. 
It uses Basic, not-capitalised Eva.


ivtff.xlsx
----------
This excel file provides a count of all locus types per page of the
Voynich MS (first worksheet). On the second worksheet this information
is summarised per quire.
The definition of the locus types may be found in the IVTFF format
definition (see PDF file described below).
The numbers for the generic types (P, L, C, R) are summed from the
numbers for the complete locus types.


RF1a-n.txt
----------
The first stable version of a reference transliteration, which was created
automatically as a combination of the GC and ZL transliterations, in the 
IVTFF 2.0 format. 
The original file was defined using the STA alphabet, and the present file 
is a simplification/approximation using Basic, not-capitalised Eva.


voyn_101.txt
------------
The original and unmodified v101 transliteration file by GC.
High-ascii characters are represented as single (high-ascii) bytes.


VT0e-n.txt
----------
The transliteration by Takeshi Takahashi, as included in the web site /
application at voynichese.com , in the IVTFF 2.0 format.
This file differs from the IT2a-n file only in details related to unreadable
characters.
It uses Basic, not-capitalised Eva.


ZL3a-n.txt
---------------
The latest release of the Zandbergen-Landini transliteration of 1999 
in the IVTFF 2.0 format. 
It is a complete transliteration, including all 5389 loci that have 
been identified in the MS. It uses the Eva alphabet, including the 
high-ascii extensions.
The file has been corrected in numerous places. Some parts of the text
inside folds of the pages still need to be added.

