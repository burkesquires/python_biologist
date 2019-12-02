#!/usr/bin/env python
"""
    Implements sequence utilities for pybioviz
    Created June 2019
    Copyright (C) Damien Farrell

    This program is free software; you can redistribute it and/or
    modify it under the terms of the GNU General Public License
    as published by the Free Software Foundation; either version 3
    of the License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
"""

import os,sys,random,subprocess
import numpy as np
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from Bio import AlignIO, SeqIO
from pyfaidx import Fasta
import pandas as pd

module_path = os.path.dirname(os.path.abspath(__file__)) #path to module
datadir = os.path.join(module_path, 'data')
templatedir = os.path.join(module_path, 'templates')
featurekeys = ['type','protein_id','locus_tag','gene','db_xref',
               'product', 'note', 'translation','pseudo','start','end','strand']

def get_template():
    
    f=open(os.path.join(templatedir, 'base.html'),'r')
    tmpl = ''.join(f.readlines())
    return tmpl

def get_css():
    """get custom css"""
    
    f=open(os.path.join(templatedir, 'custom.css'),'r')
    s=''.join(f.readlines())
    return s

def align_nucmer(file1, file2):
    """
    Align two fasta files with nucmer
    Returns: pandas dataframe of coords
    """
    
    cmd='nucmer --maxgap=500 --mincluster=100 --coords -p nucmer %s %s' %(file1, file2)
    print (cmd)
    subprocess.check_output(cmd,shell=True)
    df = read_nucmer_coords('nucmer.coords')
    return df

def read_nucmer_coords(cfile):
    """Read nucmer coords file into dataframe."""
    
    cols=['S1','E1','S2','E2','LEN 1','LEN 2','IDENT','TAG1','TAG2']
    a=pd.read_csv(cfile,sep='[\s|]+',skiprows=5,names=cols,engine='python')
    a = a.sort_values(by='TAG2',ascending=False)
    return a

def clustal_alignment(seqs):
    """Align 2 sequences with clustal"""
    
    from Bio import SeqIO, AlignIO
    filename = 'temp.fa'
    SeqIO.write(seqs, filename, "fasta")
    name = os.path.splitext(filename)[0]
    from Bio.Align.Applications import ClustalwCommandline
    cline = ClustalwCommandline("clustalw", infile=filename)
    print (cline)
    try:
        stdout, stderr = cline()        
    except:
        print ('clustalw not installed')
        return 
    align = AlignIO.read('temp.aln', 'clustal')
    return align

def muscle_alignment(seqs):
    """Align sequences with muscle"""

    from Bio import SeqIO, AlignIO
    filename = 'temp.fa'
    SeqIO.write(seqs, filename, "fasta")
    name = os.path.splitext(filename)[0]
    from Bio.Align.Applications import MuscleCommandline
    cline = MuscleCommandline(input=filename, out=name+'.txt')    
    try:        
        stdout, stderr = cline()
    except:
        print ('muscle not installed?')
        return
    align = AlignIO.read(name+'.txt', 'fasta')
    return align

def mafft_alignment(seqs):
    
    filename = 'temp.fa'
    SeqIO.write(seqs, filename, "fasta")
    cmd = 'mafft --retree 1 temp.fa > temp.aln'
    tmp = subprocess.check_output(cmd, shell=True)
    align = AlignIO.read('temp.aln', 'fasta')
    return align

def get_random_fasta(n=5):
    s=''
    for i in range(n):
        name = ''.join([random.choice(string.ascii_lowercase) for i in range(10)])
        s+='>%s\n' %name + make_seq()+'\n'    
    return s
    
def random_colors(size, seed=30):
    """random list of html colors of length sizes"""
    random.seed = seed
    
    colors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)])
                for i in range(size)]
    return colors

def get_sequence_colors(seqs, palette='viridis'):
    """Get colors for a sequence"""

    from Bio.PDB.Polypeptide import aa1
    aa1 = list(aa1)
    aa1.append('-')
    import matplotlib as mpl
    from matplotlib import cm
    pal = cm.get_cmap(palette, 256)    
    pal = [mpl.colors.to_hex(i) for i in pal(np.linspace(0, 1, 20))]
    pal.append('white')

    pcolors = {i:j for i,j in zip(aa1,pal)}
    
    text = [i for s in list(seqs) for i in s]
    clrs =  {'A':'red','T':'green','G':'orange','C':'blue','-':'white'}
    try:
        colors = [clrs[i] for i in text]
    except:
        colors = [pcolors[i] for i in text]
    return colors

def get_cons(aln):
    """Get conservation values from alignment"""

    from collections import Counter
    x=[]
    l = len(aln)
    for i in range(aln.get_alignment_length()):
        a = aln[:,i]
        res = Counter(a)
        del(res['-'])
        x.append(max(res.values())/l)
        #print (a,res,max(res.values())/l)
    return x

def get_cds(df):
    """Get CDS with translations from genbank dataframe.
    Args: pandas dataframe
    """

    cds = df[df.type=='CDS']
    cdstrans = cds[cds.translation.notnull()]
    return cdstrans

def check_tags(df):
    """Check genbank tags to make sure they are not empty.
    Args: pandas dataframe
    """

    def replace(x):
        if pd.isnull(x.locus_tag):
            return x.gene
        else:
            return x.locus_tag
    df['locus_tag'] = df.apply(replace,1)
    return df

def features_to_dataframe(features, cds=False):
    """Get features from a biopython seq record object into a dataframe
    Args:
        features: bio seqfeatures
       returns: a dataframe with a row for each cds/entry.
      """

    #preprocess features
    allfeat = []
    for (item, f) in enumerate(features):
        x = f.__dict__
        quals = f.qualifiers
        x.update(quals)
        d = {}
        d['start'] = f.location.start
        d['end'] = f.location.end
        d['strand'] = f.location.strand
        for i in featurekeys:
            if i in x:
                if type(x[i]) is list:
                    d[i] = x[i][0]
                else:
                    d[i] = x[i]
        allfeat.append(d)
    #featurekeys = list(quals.keys())+['start','end','strand','translation']
    df = pd.DataFrame(allfeat,columns=featurekeys)
    df['length'] = df.translation.astype('str').str.len()
    #print (df)
    df = check_tags(df)
    df['gene'] = df.gene.fillna(df.locus_tag)
    if cds == True:
        df = get_cds(df)
        df['order'] = range(1,len(df)+1)
    #print (df)
    if len(df) == 0:
        print ('ERROR: genbank file return empty data, check that the file contains protein sequences '\
               'in the translation qualifier of each protein feature.' )
    return df

def genbank_to_features(gb_file, key=0):
    """Read genbank record features"""
    
    if gb_file is None or not os.path.exists(gb_file):
        return
    rec = list(SeqIO.parse(open(gb_file,'r'),'genbank'))[key]
    return rec.features

def gff_to_features(gff_file):
    """Get features from gff file"""

    if gff_file is None or not os.path.exists(gff_file):
        return
    from BCBio import GFF
    in_handle = open(gff_file,'r')
    rec = list(GFF.parse(in_handle))[0]
    in_handle.close()
    return rec.features

def get_coverage(bam_file, chr, start, end):
    """Get coverage from bam file at specified region"""

    import pysam
    if bam_file is None or not os.path.exists(bam_file):
        return
    samfile = pysam.AlignmentFile(bam_file, "r")
    vals = [(pileupcolumn.pos, pileupcolumn.n) for pileupcolumn in samfile.pileup(chr, start-200, end+200)]
    df = pd.DataFrame(vals,columns=['pos','coverage'])
    df = df[(df.pos>=start) & (df.pos<=end)]
    #fill with zeroes if there is no data at ends
    if df.pos.max() < end:
        new = pd.DataFrame({'pos':range(df.pos.max(), end)})
        new['coverage'] = 0
        df = df.append(new).reset_index(drop=True)
    return df

def get_bam_ref_name(bam_file):
    """Get first ref name in bam file"""
    
    import pysam
    samfile = pysam.AlignmentFile(bam_file, "r")
    try:
        aln = samfile.fetch()
    except ValueError:
        return 
    for a in aln:
        chr = samfile.get_reference_name(a.next_reference_id)
        if chr != None:
            break    
    return chr

def get_bam_aln(bam_file, chr, start, end, group=False):
    """Get all aligned reads from a sorted bam file for within the given coords"""

    import pysam
    if not os.path.exists(bam_file):
        return
    if chr is None:
        return
    if start<1:
        start=0    
    samfile = pysam.AlignmentFile(bam_file, "r")
    iter = samfile.fetch(chr, start, end)
    d=[]
    for read in iter:
        st = read.reference_start        
        d.append([read.reference_start, read.reference_end, read.cigarstring,
                  read.query_name,read.query_length,read.mapping_quality])
    df = pd.DataFrame(d,columns=['start','end','cigar','name','length','mapq'])
    if len(df) == 0:
        return pd.DataFrame()
    if group == True:
        df['counts'] = df.groupby(['start','end']).name.transform('count')
        df = df.drop_duplicates(['start','end'])
    df['y'] = 1
    bins = (end-start)/150
    if bins < 1:
        bins = 1
    xbins = pd.cut(df.start,bins=bins)
    df['y'] = df.groupby(xbins)['y'].transform(lambda x: x.cumsum())    
    return df

def get_chrom(filename):
    """Get first sequence name in a bam file"""
    
    if filename is None:
        return ''
    import pysam
    samfile = pysam.AlignmentFile(filename, "r")
    try:
        iter=samfile.fetch(start=0,end=10)
    except ValueError:
        return
    for read in iter:
        if read.reference_name:
            return read.reference_name
        
def get_fasta_sequence(filename, start, end, key=0):
    """Get chunk of indexed fasta sequence at start/end points"""
    
    from pyfaidx import Fasta
    refseq = Fasta(filename)
    if type(key) is int:
        chrom = list(refseq.keys())[key]   
    seq = refseq[chrom][start:end].seq
    return seq

def get_fasta_length(filename):
    """Get length of reference sequence"""

    refseq = Fasta(filename)
    key = list(refseq.keys())[0]
    l = len(refseq[key])
    return l

def get_fasta_names(filename):
    """Get names of fasta sequences"""

    refseq = Fasta(filename)
    return list(refseq.keys())

def vcf_to_dataframe(vcf_file, quality=30):
    """Read vcf into dataframe"""
    
    import vcf
    vcf_reader = vcf.Reader(open(vcf_file,'r'))   
    res=[]    
    for rec in vcf_reader:
        x = rec.CHROM, rec.var_type, rec.var_subtype, rec.start, rec.end, str(rec.REF), str(rec.ALT), rec.QUAL, rec.INFO['DP'] ,rec.INFO['AO'][0],rec.INFO['RO']
        #print rec, rec.INFO['DP'] ,rec.INFO['RO']
        res.append(x)
    res = pd.DataFrame(res,columns=['chrom','var_type','sub_type','start','end','REF','ALT','QUAL','DP','AO','RO']) 
    res = res[res.QUAL>=quality]
    return res
