import os
import csv
import numpy as np
from random import seed
from random import randint
from random import choice

def random_dnasequence(size):
    """
    Generate random sequence of DNA

    Parameters
    ----------
    size : Size of DNA in bp
      An integer between 1 and 100 000 000.

    Returns
    -------
    string
      A string corresponding to DNA sequence.

    Examples
    --------
    >>> from insilicogenome import insilicogenome
    >>> insilicogenome.random_dnasequence(10)
    'TGCTTGATGG'
    """
    if ((size>= 0) and (size<= 100000000)):
        pass
    elif (size > 100000000):  # on a title line
        raise ValueError(
            "The size of the sequence to generate is greater than the maximum size of 100000000bp"
            f"The value of '{size}' is too big, it must be reduced"
        )
    else:
        assert size > 0, "Size value negatif ; this should be impossible!"
    np.random.seed(123)
    sequence = ''.join(np.random.choice(('C','G','T','A'), size, p=[0.25, 0.25, 0.25, 0.25] ))
    return sequence

def reverse_complement(dna):
    """
    Replace a sequence to get reverse complement

    Parameters
    ----------
    dna : DNA sequence
      Sequence contening only A/T/C/G.

    Returns
    -------
    string
      A string corresponding to the reverse complement of DNA sequence.

    Examples
    --------
    >>> from insilicogenome import insilicogenome
    >>> insilicogenome.reverse_complement("TGCTTGATGG")
    'CCATCAAGCA'
    """
    assert "U" not in dna,'Error: reverse complement a RNA instead of DNA ("U" within sequence)'
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'} 
    return ''.join([complement[base] for base in dna[::-1]])

def replace_start_codons(sequence, codon_start_array = ["ATG", "CAT", "TTG", "CAA", "CTG", "CAG"]):
    """
    Replace all the occurence of initiation codon by random sequence {ATG & CAT, TTG & CAA, CTG & CAG}.
    The CAT, CAA, CAG are the reverse complement sequence of classical start codon

    Parameters
    ----------
    sequence : A sequence of DNA between 1 and 100 000 000bp
      A string generated by random_dnasequence

    Returns
    -------
    string
      A string corresponding to DNA sequence without start codons.

    Examples
    --------
    >>> from insilicogenome import insilicogenome
    >>> insilicogenome.replace_start_codons("GTTCTTGAT")
    'GTTCCCCAT'
    """
    iteration=0
    while (codon_start_array[0] in sequence or codon_start_array[1] in sequence or codon_start_array[2] in sequence):
        if (iteration == 1000):
            break
        else:
            tempRecordSeq = list(sequence)
            np.random.seed(iteration)
            for index in range(0, len(sequence), 1):
                    codon = sequence[index:index+3]
                    if codon in codon_start_array:
                        tempRecordSeq[index:index+3] = np.random.choice(('C','G','T','A'), 3, p=[0.25, 0.25, 0.25, 0.25] )
            sequence = "".join(tempRecordSeq)
            iteration += 1
    return sequence

def insert_random_gene(sequence, start, stop, codon_start=None, codon_stop=None, strand="+"):
    """
    Insert codon start and stop in sequence to add a gene

    Parameters
    ----------
    sequence : A sequence of DNA between 1 and 100 000 000bp
      A string generated by random_dnasequence
    start : The location of the gene start in relation to the genome
      An integer that will be at least 6 positions before the stop
    stop : : The location of the gene start in relation to the genome
      An integer that will be at least 6 positions after the start
    codon_start : The codon where the gene starts {"ATG", "TTG", "CTG"}
      By default a codon will be chosen randomly between the 3 possible ones
    codon_stop : The codon where the gene stop {"TAG", "TAA", "TGA"}
      By default a codon will be chosen randomly between the 3 possible ones
    strand : The strand on which the gene will be found, if '+' the orientation will be 5' to 3', if '-' the orientation will be 3' to 5'
      By default it will be '+' and the orientation will be 5' to 3'.
    name : the name of the gene used, mainly used to facilitate debugging

    Returns
    -------
    string
      A sequence with a random gene inserted at the requested position.

    Examples
    --------
    >>> from insilicogenome import insilicogenome
    >>> insilicogenome.insert_random_gene("GTTCTTGATGTTCTTGAT", 2, 14)
    'GTCTGTTCTTGATGTAGT'

    >>> insilicogenome.insert_random_gene("GTTCTTGATGTTCTTGAT", 2, 14, codon_start="ATG", codon_stop="TAA", strand = "-")
    'GTCATTTCTTGATGTTAT'
    """
    np.random.seed(123)
    #assert codon_stop not in codon_stop_array,'Error in codon stop definition, provide "TAG", "TAA", "TGA"'
    assert len(
        sequence) > 6, f"Error in gene size pos {start}-{stop} due to a sequence size inferior to 6bp"
    if ((stop - start + 1) > 75):
        pass
    else:
        print(
            f"Warning: Gene size is abnormally small, check gene size in pos {start}-{stop}")
      	# warnings.warn('Gene size is abnormally small, check gene size', DeprecationWarning) # pb dependancy poetry
    # control codon start
    codon_start_array = ["ATG", "TTG", "CTG"]
    if codon_start is None:
        codon_start = np.random.choice(
            codon_start_array, 1, p=[0.34, 0.33, 0.33])
    else:
        assert codon_start in codon_start_array, 'Error in codon start definition, provide "ATG", "TTG", "CTG"'
    # control codon stop
    codon_stop_array = ["TAG", "TAA", "TGA"]
    if codon_stop is None:
        codon_stop = np.random.choice(
            codon_stop_array, 1, p=[0.34, 0.33, 0.33])
    else:
        assert codon_stop in codon_stop_array, 'Error in codon stop definition, provide "TAG", "TAA", "TGA"'
    # Check if frame is respected
    if ((stop-start) % 3) == 0:
        pass
    else:
        raise ValueError(
            f"position of start and stop codon on the gene position {start}-{stop} \
                is not in the same frame stop-start)%3 ={(stop-start)%3}")
    # modified sequence
    if strand == "+":
        return sequence[:start] + ''.join(codon_start) + sequence[(start+3)] + \
            sequence[start:(stop-4)] + ''.join(codon_stop) + sequence[(stop+3):]
    elif strand == "-":
        return sequence[:start] + reverse_complement(''.join(codon_start)) + sequence[(start+3)] + \
            sequence[start:(stop-4)] + reverse_complement(''.join(codon_stop)) + sequence[(stop+3):]
    else:
        raise ValueError(
            f"Error on 'strand' parameter in gene pos {start}-{stop} change {strand} to '+' or '-'")


# Ce fichier pourrait allé dans un autre module.
def random_table_genes(random_table_genes_file, size, genes_numbers=1):
  """
  docstring
  random_table_genes("~/Téléchargements/random_table_genes.csv", 1000, genes_numbers=3)
  """
  with open(random_table_genes_file, 'w', encoding='UTF8', newline='') as csv_file:
    writer = csv.writer(csv_file)
    seed(1)
    i=1
    while i <= genes_numbers:
        start=randint(0,size-6)
        data = [start,(start+3*randint(1,150)), choice(["+","-"])]
        writer.writerow(data)
        i += 1

def insert_table_genes(sequence, genes):
    """
    docstring 
    """
    if os.path.isfile(genes):
        pass
    else:
        raise FileExistsError
    with open('readme.txt') as csv_file:
      lines = f.readlines()
  
  

def write_fasta_genome(output, sequence):
    """
    Writes name/sequence to file in FASTA format

    Parameters
    ----------
    output : The name of the header and fasta file
      A string containing the path
    sequence : A sequence of DNA between 1 and 100 000 000bp
      A string generated by random_dnasequence

    Returns
    -------
    None

    Examples
    --------
    >>> from insilicogenome import insilicogenome
    >>> insilicogenome.write_fasta_genome(/path/genome.fasta, 'GTTCTTGAT')
    """
    # Confirm path make sens, and allow absolut path
    if os.path.isfile(output):
        raise FileExistsError
    # Raise error if not only ACTG in sequence to avoid inversion
    header=os.path.basename(output)
    header=os.path.splitext(header)[0]
    n = 70	# return line every 70 characters
    split_sequence = [sequence[i:i+n] for i in range(0, len(sequence), n)]
    with open(output, 'w') as outfile:
            outfile.write(f">{header}\n")
            for item in split_sequence:
                outfile.write(f"{item}\n")