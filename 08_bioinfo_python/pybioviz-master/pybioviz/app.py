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

import os,sys,subprocess
import pandas as pd
from . import dashboards, utils, __version__

def run_server(appname, path='.', filename='', gff_file=None, ref_file=None, 
               bam_file=None, port=8000, **kwargs):
      
    if appname == 'test':
        app = dashboards.test_app()
    elif appname == 'align':
        app = dashboards.sequence_alignment_viewer(filename)
    elif appname == 'features':
        app = dashboards.genome_features_viewer(gff_file, ref_file)
    elif appname == 'bam':
        app = dashboards.bam_viewer(bam_file, ref_file, gff_file, width=1000)
    else:
        print ('valid dashboard names: test, align, bam, features')
        return
    if app is None:
        print ('please provide the correct input files')
        return
    from bokeh.server.server import Server
    def modify_doc(doc):               
        return app.server_doc(doc=doc, title='pybioviz: %s' %appname)
        
    server = Server({'/': modify_doc}, port=port)
    print('Opening application on http://localhost:%s/' %server.port)
    server.start()
    server.show('/')
    server.run_until_shutdown()
    return

def main():
    "Run the application"

    import sys, os
    from argparse import ArgumentParser
    parser = ArgumentParser(description='pybioviz command line tools')

    parser.add_argument(dest="appname", default='test',
                        help="dashboard name: test, align, features")
    parser.add_argument("-f", "--fasta", dest="filename",
                        help="input fasta file", metavar="FILE")
    parser.add_argument("-r", "--ref", dest="ref_file",
                        help="reference fasta file", metavar="FILE")
    parser.add_argument("-g", "--gff", dest="gff_file",
                        help="gff file", metavar="FILE")    
    parser.add_argument("-b", "--bam", dest="bam_file",
                        help="bam file", metavar="FILE")    
    parser.add_argument("-p", dest="port", default=None,
                        help="Port to use, random if none provided")    
    args = vars(parser.parse_args())
        
    run_server(**args)        
        
if __name__ == '__main__':
    main()
