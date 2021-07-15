from insilicogenome import __version__
from insilicogenome import insilicogenome
from Bio.Seq import Seq
import numpy as np

def test_version():
    assert __version__ == '0.1.0'

def test_random_dnasequence():
    size = 10
    assert ((insilicogenome.random_dnasequence(size)) == 'TGCTTGATGG')

def test_replace_start_codons():
    assert ((insilicogenome.replace_start_codons("ATGATGAAATTCCTTGCATTT")) == 'GCTTCTAAATTCCGAAGATTT')