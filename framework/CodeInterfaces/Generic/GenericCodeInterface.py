'''
Created March 17th, 2015

@author: talbpaul
'''
from __future__ import division, print_function, unicode_literals, absolute_import
import warnings
warnings.simplefilter('default',DeprecationWarning)

import os
import copy
from CodeInterfaceBaseClass import CodeInterfaceBase

class GenericCodeInterface(CodeInterfaceBase):
  def __init__(self):
    CodeInterfaceBase.__init__(self) #I think this isn't implemented
    self.inputExtensions  = [] #list of extensions for RAVEN to edit as inputs
    self.outputExtensions = [] #list of extensions for RAVEN to gather data from?
    self.execPrefix       = '' #executioner command prefix (e.g., 'python ')
    self.execPostfix      = '' #executioner command postfix (e.g. -zcvf)
    self.caseName         = None #base label for outgoing files, should default to inputFileName


  def _readMoreXML(self,xmlNode):
    for chid in xmlNode:
      if child.tag == 'inputExtentions':
        extdict = {'input':str(child.text).strip().split(',')}
        self.setExtensions(extdict) #TODO fix with whatever Andrea calls it
      elif child.tag == 'outputExtension':
        extdict = {'output':str(child.text).strip()}
        self.setExtensions(extdict) #TODO fix with whatever Andrea calls it
      elif child.tag == 'executablePrefix':
        self.execPrefix = str(child.text)+' '
      elif child.tag == 'executablePostfix':
        self.execPostfix = ' '+str(child.text)
      elif child.tag == 'caseName':
        self.caseName = caseName

  def generateComand(self,inputFiles,executable,flags=None):
    #inputFiles -> list of input files
    found = False
    for index,inputFile in enumerate(inputFiles):
      if inputFiles.endswith(tuple(self.inputExtensions)): #TODO fix with whatever Andrea calls it
        #FIXME what about multiple input files?
        found = True
        break
    if not found: raise IOError('GENERIC INTERFACE ERROR -> No input file with '+str(self.inputExtensions)+' extension found!')
    if self.caseName == None: self.caseName=os.path.split(inputFiles[index])[1].split('.')[0]
    outfile = 'out~'+self.caseName
    executeCommand = (self.execPrefix+executable+self.execPostfix)
    #TODO how to specify where the output is set?  -> for now, use special keyword $RAVEN-outFileName$

  def createNewInput(self,currentInputFiles,origInputFiles,samplerType,**Kwargs):
    import GenericParser
    indexes=[]
    infiles=[]
    for index,inputFile in enumerate(inputFiles):
      if inputFile.endswith(self.getInputExtension()):
        indexes.append(index)
        infiles.append(inputFile)
    parser = GenericParser.GenericParser(infiles) #TODO this is a list, so be careful
    parser.modifyInternalDictionary(**Kwargs['SampledVars'])
    temps = list(str(oriInputFiles[i][:]) for i in indexes)
    newInFiles = copy.deepcopy(currentInputFiles)
    for i in indexes:
      newInFiles[i] = os.path.join(os.path.split(temp)[0],Kwargs['prefix']+'~'+os.path.split(temp)[1])
    parser.writeNewInput(list(newInFiles[i] for i in indexes))
    return newInFiles
