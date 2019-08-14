from datetime import datetime

debugmode=False

def addLog(logLevel,line):
 lstamp = datetime.now().strftime('%H:%M:%S')
 global debugmode
 if (int(logLevel)==0) or (int(logLevel)==1 and debugmode):
  print(lstamp+" : "+line)
