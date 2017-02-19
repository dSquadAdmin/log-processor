import re
import os
import sys
from datetime import datetime
class LogProcessor:

    def __init__(self, files, out_dir = os.path.expanduser('~')+'/logproc', write=0): # if write =1 data is written to log file, default value is 0
        self.__files = files
        self.output_dir = out_dir
        self.write = write
        self.summary = {}
        self.key_summary = {}
        self.outfile = self.output_dir+'/summary-'+str(datetime.now().strftime("%Y-%m-%d-%H-%M"))+'.log'
        if write==1:
            self.check_logproc_dir()

    def check_logproc_dir(self): # check if specified directory is present else create it
        print 'Searching for the directory [%s]'%(self.output_dir)
        try:
            os.listdir(self.output_dir)
            print 'Directory found'
        except OSError:
            print 'Directory not found, creating it'
            try:
                os.mkdir(self.output_dir)
            except OSError:
                print 'I cannot create directory, exiting ...'
                sys.exit()
            
    
    def compute(self):
        for filename in self.__files:
            self.process(os.path.abspath(filename))  
        if self.write==1:
            print '\nData logged to [%s]'%(self.outfile)      

### this method contanis main logic to compute the result from processing
    def process(self, filename):
        last_key = ''
        try:
            fileobj = open(filename)
            print '[Processing:] %s'%(filename)
            for line in fileobj:
                dateId = re.match(r'\d\d\d\d-\d\d-\d\d', line)
                identity = dateId.group()
                if self.summary.has_key(identity):
                    data = self.summary[identity]
                    warn = re.search(r'\bwarning\b', line)
                    err = re.search(r'\berror\b', line)
                    if warn!=None:
                        data['Warnings'] +=1
                    elif err!=None:
                        data['Errors']+=1
                    self.summary[identity] = data
                    self.key_summary[identity] = data 

                else:
                    data = {'Warnings':0, 'Errors':0}
                    if self.write ==1:  # if write is enabled write the log to the file
                        if last_key != identity and len(self.summary)!=0:
                            self.write_summary()
                            last_key = identity
                            self.key_summary = {}

                    warn = re.search(r'\bwarning\b', line)
                    err = re.search(r'\berror\b', line)
                    if warn!=None:
                        data['Warnings'] += 1
                    elif err!=None:
                        data['Errors'] += 1
                    self.summary[identity] = data
                    self.key_summary[identity] = data  

            fileobj.close()

        except IOError:
            print '[Error Opening ] %s, Skipping it ..'%(filename)


    def write_summary(self): # this method logs the summarized result to the file
        if len(self.key_summary)==0:
            return
        day_summary = ''
        key = self.key_summary.keys()[0]
        data_summary = self.key_summary[key]
        day_summary = str(key)+" warning: "+str(data_summary['Warnings'])+" error: "+str(data_summary['Errors'])
        try:
            output = open(self.outfile, 'a+')
            output.write(day_summary+"\n")
            output.close()
        except IOError:
            print 'I was unable to write data to the output file, Exiting'
            sys.exit()

   ## Methods to display results
    def display_result_from_file(self):
        try:
            result_file = open(self.outfile)
            print '\nLog Summary:'
            for line in result_file:
                print line
        except IOError:
            print 'Error while reading log, displaying result from memory'
            self.display_result_from_file()

    def display_result_from_memory(self):
        print '\nLog Summary:'
        keys = self.summary.keys()
        keys.sort()
        for key in keys:
            data = self.summary[key]
            msg = str(key)+' warning: '+str(data['Warnings'])+' error: '+str(data['Errors'])
            print msg
