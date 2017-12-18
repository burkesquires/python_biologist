#! /bin/bash
###
### Exercise 1 - basics of rules
###
#
# turn this script first into a snakefile. First use specific
# file names, then generalize the rule to work on any fastq file
# in the 00fastq directory.

module load hisat/2.0.5 samtools/1.4
idx=00ref/hisat_index/R64-1-1
mkdir -p 02aln
hisat2 -x $idx -U 00fastq/ERR458495.fastq.gz --threads 4 \
  | samtools sort -T tmp/ERR458495 -O BAM \
  > 02aln/ERR458495.bam
samtools index 02aln/ERR458495.bam
