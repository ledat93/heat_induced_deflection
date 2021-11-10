import os, json 

##-- get parameters
pfile   = open('param.json')
par     = json.load(pfile)
pfile.close()

##-- change directory
def change_dir(dfolder = str()):
    if len(dfolder) == 0:
        dfolder = 'Data/'
    if os.path.isdir(dfolder):
        print('Existed folder: ', dfolder)
    else:
        os.mkdir(dfolder)
        print('Created folder: ', dfolder)
    os.chdir(dfolder)
    print('Current directory: ', os.getcwd())
    
    
if __name__=='__main__':
    from deflection import LaserSource, runCalculation
    laser = LaserSource()
    laser.deltaSource(par)
    Tx, Zx = runCalculation(0.5, laser, par)    
    change_dir()     
    isSimulation = input('Would you like to run simulation? (t|temperature or d|deflection): ', )
    data = None
    if str(isSimulation) == 't':
        data = Tx 
    elif str(isSimulation) == 'd':
        data = Zx
    else:
        print('Your enter donot support!!!')
        exit()    
    nfile = input('Data will be written into: ', ) 
    with open(str(nfile), 'w') as f:        
        for x,value in data:
            line = ','.join([str(x),str(value)])
            f.write(line)
            f.write('\n')                
    print('Done')