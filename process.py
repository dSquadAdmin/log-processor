import os
import re
import sys
import argparse
from logprocessor import *

ABOUT = 'Log file processor, it summarises the errors and warnings in a log files. Files must have .log extension. Assign any number of files for processing.'
ABOUT_AUTHOR = 'Program by: Keshav Bist <squad.reconn@gmail.com>, http://keshavbist.com.np'

arguments = ''

def sanetize(arguements):
    """ sanetize(arguements) -> sanetizedvalues
    This method filters the non log files supplied to the program,
    Removes the files with extension other than .log""" 
    sanetizedvalues = []
    for token in arguements:
        result = re.search(r'\b.log\b$', token)
        if result != None:
            sanetizedvalues.append(token)
    return sanetizedvalues


def init_proc(parser):
    args = parser.parse_args()
    print 'Initiating the Log Processor...'
    if args.files==None:
        parser.print_help()
        sys.exit()
        
    arguments = sanetize(args.files) ## Remove non logged files
    
    if len(arguments)==0:
        print 'No any log files found'
        parser.print_help()
        sys.exit()
    
    if args.output==None:
        if args.enable:
            print 'Logging enabled with output directory specified, summarized data will be written in ~/logproc/'
            logproc = LogProcessor(arguments, os.path.expanduser('~')+'/logproc', 1)
        else:
            print 'Logging not enabled, Summary of the processor will not be stored in any files'
            logproc = LogProcessor(arguments)
    else:
        print 'Output Directory: %s'%(args.output)
        logproc = LogProcessor(arguments, args.output, 1)
 
    return args, logproc


def main():
    parser = argparse.ArgumentParser(description=ABOUT, epilog=ABOUT_AUTHOR)
    parser.add_argument("-f", "--files", nargs='+', help='List of files to be processed, atleast one log file must be supplied.')
    parser.add_argument('-o', '--output', nargs='?', help='Specifies output directory where summarized file is to be written, It is optional.')
    parser.add_argument('-e', '--enable', help ='Specifies to write data to summary file,'+
                                                ' If used with -f, it logs summary to ~/logproc/ directory,'+
                                                ' It is enabled by default with -o flag. It is optional, but adviced to enable logging.', 
                                                action='store_true')
    args, logproc = init_proc(parser)
    logproc.compute() ## compute the count for error and warning
    if args.enable:
        logproc.display_result_from_file()
    else:
        logproc.display_result_from_memory()

if __name__ =="__main__":
    main()

