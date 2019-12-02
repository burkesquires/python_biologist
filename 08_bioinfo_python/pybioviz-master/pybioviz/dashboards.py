#!/usr/bin/env python
"""
    Implements viewers/panel apps for pybioviz
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

import os,sys,io
import numpy as np
import pandas as pd
from . import utils, plotters
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.Align import MultipleSeqAlignment
from Bio import AlignIO, SeqIO

from bokeh.plotting import figure
from bokeh.models import (ColumnDataSource, Plot, LinearAxis, Grid, Range1d,CustomJS, Slider, HoverTool)
from bokeh.models.glyphs import Text, Rect
from bokeh.layouts import gridplot, column
import panel as pn
import panel.widgets as pnw

def test_app():
    """Test dashboard"""
    
    def refresh(event):
        plot1.object = plotters.test1(cols=col_sl.value,rows=row_sl.value, plot_width=600)
        plot2.object = plotters.test2(rows=row_sl.value, plot_width=600)
        return
    from . import __version__
    title = pn.pane.Markdown('# pybioviz v%s test plots' %__version__)
    plot1 = pn.pane.Bokeh()   
    plot2 = pn.pane.Bokeh()
    col_sl = pnw.IntSlider(name='cols',value=30,start=5,end=200,step=1)
    col_sl.param.watch(refresh, 'value')
    row_sl = pnw.IntSlider(name='rows',value=10,start=5,end=100,step=1)
    row_sl.param.watch(refresh, 'value')
    col_sl.param.trigger('value')    
    app = pn.Column(title,col_sl,row_sl,plot1,plot2)
    return app

def sequence_alignment_viewer(filename=None):
    """Sequence alignment viewer"""
    
    title = pn.pane.Markdown()
    aln_btn = pnw.Button(name='align',width=100,button_type='primary')
    file_input = pnw.FileInput(name='load file',width=100,accept='.fa,.fasta,.faa')
    aligner_sel = pnw.Select(name='aligner',value='muscle',options=['muscle','clustal','maaft'],width=100)
    highlight_sel = pnw.Select(name='highlight mode',value='default',options=['default',''],width=100)
    rowheight_sl = pnw.IntSlider(name='row height',value=10,start=5,end=20,width=120)
    seq_pane = pn.pane.HTML(name='sequences',height=200,css_classes=['scrollingArea'])
    bokeh_pane = pn.pane.Bokeh()

    def update_title(filename):
        title.object = '### Sequence aligner: %s' %filename
        
    def update_file(event):        
        nonlocal seqtext
        seqtext = file_input.value.decode('utf-8')
        title.object = file_input.filename
        update_title(file_input.filename)
        return

    def align(event):
        #this function does the alignment
        nonlocal seqtext        
        if seqtext is not None:
            sequences = SeqIO.parse(io.StringIO(seqtext),format='fasta')
        elif filename is not None:    
            sequences = SeqIO.parse(filename, format='fasta')
        else:      
            return
        sequences = list(sequences)
        #print (sequences)
        aligner = aligner_sel.value
        if aligner == 'muscle':
            aln = utils.muscle_alignment(sequences)    
        elif aligner == 'clustal':
            aln = utils.clustal_alignment(sequences)
        elif aligner == 'mafft':
            aln = utils.mafft_alignment(sequences)
        if aln is None:
            bokeh_pane.object = plotters.plot_empty('%s not installed?' %aligner,900)
        else:
            #the bokeh pane is then updated with the new figure
            bokeh_pane.object = plotters.plot_sequence_alignment(aln, row_height=rowheight_sl.value)  
        return 
   
    seqtext = None
    file_input.param.watch(update_file,'value')
    rowheight_sl.param.watch(align,'value')
    aln_btn.param.watch(align, 'clicks')
    aln_btn.param.trigger('clicks')
    update_title(filename)
    side = pn.Column(aln_btn,file_input,aligner_sel,highlight_sel,rowheight_sl,seq_pane,css_classes=['form'],width=200,margin=20)   
    app = pn.Column(title,pn.Row(side, bokeh_pane), sizing_mode='stretch_width',width_policy='max',margin=20)
    return app

def genome_features_viewer(gff_file, ref_file=None, plot_width=900):
    """Gene feature viewer app"""
    
    if gff_file is None:
        return
    
    features = utils.gff_to_features(gff_file)
    df = utils.features_to_dataframe(features)
    
    loc_pane = pnw.TextInput(name='location',value='',width=150)
    search_pane = pnw.TextInput(name='find_gene',value='',width=220)
    slider = pnw.IntSlider(name='start',start=0,end=10000,step=500,value=1,width=plot_width)
    xzoom_slider = pnw.IntSlider(name='zoom',start=1,end=500,value=100,step=5,width=100)
    chrom_select = pnw.Select(name='chrom',width=220)
    left_button = pnw.Button(name='<',width=40)
    right_button = pnw.Button(name='>',width=40)
    
    feature_pane = pn.pane.Bokeh(height=100,margin=10)
    seq_pane = pn.pane.Bokeh(height=50,margin=10)
    debug_pane = pn.pane.Str('debug',width=200,style={'background':'yellow','margin': '4pt'})
    
    if ref_file is not None:
        seqlen = utils.get_fasta_length(ref_file)
        slider.end = seqlen
    else:
        slider.end = int(df.end.max())

    def search_features(event):
        """Find a feature"""
        
        term = search_pane.value        
        feats = utils.gff_to_features(gff_file)
        df = utils.features_to_dataframe(feats)    
        df['gene'] = df.gene.fillna('')
        f = df[df.gene.str.contains(term)].iloc[0]
        #debug_pane.object = str(f.start)
        slider.value = int(f.start)-100
        update(event)
        return   
    
    def pan(event):
        p = feature_pane.object
        rng = p.x_range.end-p.x_range.start        
        inc = int(rng/10)
        print (event.obj.name)
        if event.obj.name == '<':
            slider.value = int(slider.value) - inc        
        else:
            slider.value = int(slider.value) + inc   
        update(event)
        return
    
    def update(event):      
        print (event.obj.name)
        if event.obj.name in ['start', 'zoom']:
            xzoom = xzoom_slider.value*200
            start = int(slider.value)
            N = xzoom/2
            end = int(start+N)
            loc_pane.value = str(start)+':'+str(end)            
        elif event.obj.name == 'location':            
            vals = loc_pane.value.split(':')
            start = int(vals[0])
            end = int(vals[1])
            slider.value = start        
            
        #debug_pane.object=type(start)
        p = feature_pane.object
        p.x_range.start = start
        p.x_range.end = end
        if ref_file:
            sequence = utils.get_fasta_sequence(ref_file, start, end)
            seq_pane.object = plotters.plot_sequence(sequence, plot_width, plot_height=50,fontsize='9pt',xaxis=False)            
        return
        
    slider.param.watch(update,'value',onlychanged=True)
    #slider.param.trigger('value')    
    xzoom_slider.param.watch(update,'value')       
    search_pane.param.watch(search_features,'value')    
    loc_pane.param.watch(update,'value',onlychanged=True)    
    left_button.param.watch(pan,'clicks')
    right_button.param.watch(pan,'clicks')
    #debug_pane.object = utils.get_fasta_names(ref_file)[0] 
    if ref_file != None:
        chrom_select.options = utils.get_fasta_names(ref_file)
    #plot
    p = feature_pane.object = plotters.plot_features(features, 0, 10000, plot_width=plot_width, tools="", rows=4)
    
    #side = pn.Column(file_input,css_classes=['form'],width=200,margin=20)
    top = pn.Row(loc_pane,xzoom_slider,search_pane,chrom_select,left_button,right_button)
    main = pn.Column(feature_pane, seq_pane, sizing_mode='stretch_width')
    app = pn.Column(top,slider,main,debug_pane, sizing_mode='stretch_width',width_policy='max',margin=20)
    return app

def bam_viewer(bam_file, ref_file, gff_file=None, width=1000, height=200, color='gray'):
    """Bam viewer widget.
    
    Args:
        bam_file: sorted bam file
        ref_file: reference sequence in fasta format
        gff_file: optional genomic features file
    """
    slider = pnw.IntSlider(name='location',start=1,end=10000,value=500,step=500,width=300)
    main_pane = pn.pane.Bokeh(height=100)
    cov_pane = pn.pane.Bokeh(height=60)
    loc_pane = pn.pane.Str(50,width=250,style={'margin': '4pt'})
    feat_pane = pn.pane.Bokeh(height=60)
    ref_pane = pn.pane.Bokeh(height=60)
    xzoom_slider = pnw.IntSlider(name='x zoom',start=50,end=8000,value=1000,step=10,width=100)
    yzoom_slider = pnw.IntSlider(name='y zoom',start=10,end=100,value=20,step=5,width=100)#,orientation='vertical')
    panleft_btn = pnw.Button(name='<',width=50,button_type='primary')
    panright_btn = pnw.Button(name='>',width=50,button_type='primary')
    chroms_select = pnw.Select(name='Chromosome', options=[], width=250)
    colorby = pnw.Select(name='Color by', options=['quality','pair orientation','read strand'], width=180)
    search_pane = pnw.TextInput(name='search',width=200)
    trans_option = pnw.Checkbox(name='show translation')
    debug_pane = pn.pane.Markdown()
    
    def pan_right(event):
        plot = main_pane.object
        plot.x_range
        start = slider.value 
        loc = slider.value+100    
        slider.value=loc
        update(event)
        return

    def pan_left(event):
        loc = slider.value-100
        if loc<1:
            return
        slider.value=loc
        update(event)
        return

    def update_features():
        """Load features"""

        if gff_file is None:
            return        
        ext = os.path.splitext(gff_file)[1]        
        if ext in ['.gff','.gff3']:
            feats = utils.gff_to_features(gff_file)
        elif ext in ['.gb','.gbff']:
            feats = utils.genbank_to_features(gff_file)
        p = feat_pane.object = plotters.plot_features(feats, 
                                                  plot_width=width, plot_height=100)
        return p

    def search_features(event):
        """Find a feature"""
        
        term = search_pane.value        
        feats = utils.gff_to_features(gff_file)
        df = utils.features_to_dataframe(feats)    
        df['gene'] = df.gene.fillna('')
        f = df[df.gene.str.contains(term)].iloc[0]
        debug_pane.object = str(f.start)
        slider.value = int(f.start)
        update(event)
        return
    
    def update_ref(filename, start, end):
        """Update reference sequence"""

        if filename == None:
            return
        seqlen = utils.get_fasta_length(filename)
        slider.end = seqlen
        refseq = Fasta(filename)
        chroms = list(refseq.keys())
        chroms_select.options = chroms
        key = chroms[0]
        seq = refseq[key][int(start):int(end)].seq
        ref_pane.object = plotters.plot_sequence(seq, plot_height=50,fontsize='9pt',xaxis=False)
        return
    
    def update(event):
        """Update viewers on widget change"""

        xzoom = xzoom_slider.value
        yzoom = yzoom_slider.value
        start = slider.value     
        N = xzoom/2
        end = start+N
        chrom = utils.get_chrom(bam_file)
        loc_pane.object = '%s:%s-%s' %(chrom,start,int(end))
        cov = utils.get_coverage(bam_file,chrom,start,end)
        cov_pane.object = plotters.plot_coverage(cov,plot_width=width)
        main_pane.object = plotters.plot_bam_alignment(bam_file,chrom,start,end,height=yzoom,plot_width=width,plot_height=height)        
        update_ref(ref_file, start, end)
        if feature_plot:
            feature_plot.x_range.start = start
            feature_plot.x_range.end = end
        debug_pane.object = ''
        return

    slider.param.watch(update, 'value')
    xzoom_slider.param.watch(update, 'value')
    yzoom_slider.param.watch(update, 'value')
    panright_btn.param.watch(pan_right, 'clicks')
    panleft_btn.param.watch(pan_left, 'clicks')
    search_pane.param.watch(search_features, 'value')
    feature_plot = update_features()
    
    #initialise slider
    slider.param.trigger('value')
    
    #menus = pn.Row(bam_input, ref_input, gff_input)
    top = pn.Row(slider,xzoom_slider,yzoom_slider,panleft_btn,panright_btn,loc_pane)
    bottom = pn.Row(chroms_select, search_pane,colorby,trans_option)
    app = pn.Column(top,cov_pane,main_pane,ref_pane,feat_pane,bottom,debug_pane)
    return app