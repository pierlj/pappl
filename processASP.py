import os

def processASP(path):
    file=open(path,'r')
    lines=file.readlines()
    correle=lines[occur("correle",lines)]
    correleSep=correle.split()
    file.close()
    name=os.path.splitext(path)[0]+"-processed"+os.path.splitext(path)[1]
    print(name)
    file=open(name,'w')
    for line in correleSep:
        file.write(line+"\n")
    file.close()
        
    
    
    
def occur(m,l):
    for k in range(len(l)):
        if(m in l[k]):
            return k
    