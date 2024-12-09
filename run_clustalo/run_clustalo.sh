#!/bin/bash
input_base="/Users/RBKothadia/Documents/code/avalos/refactored_fasta_dumps/"
input_fasta_ilvc=$input_base"/14_ilvC_E.coli_refactored_trimmed.fa"
input_fasta_ilvd=$input_base"/15_ilvD_E.coli_refactored_trimmed.fa"

clustalo \
  -i $input_fasta_ilvc \
  -o alignment_ilvc.out \
  --distmat-out=distance_matrix_ilvc.txt --full -v

clustalo \
  -i $input_fasta_ilvd \
  -o alignment_ilvd.out \
  --distmat-out=distance_matrix_ilvd.txt --full -v
