import sys
import numpy as np
import matplotlib.pyplot as plt
# Append paths to sys.path
path_to_rpa = __path_to_rpa__
sys.path.append('path_to_rpa')
sys.path.append('path_to_rpa')

from BoundaryFit import *
from MapFit import *

chiAB = 0.1326
chiAS = 0.632
chiBS = 0.369
dfA = 0.05
dphip = 0.02


fAlist = np.arange(0.0,1.0+1e-6,dfA)
phiPlist = np.arange(0.0,1.0+1e-6,dphip)
N = 150
bA = 1.0
bB = 0.6

# define map
basename = 'ABS'
args = {'filename':f'../{basename}_{N}.npy','load_form_factor':True,'export_filename':f'../{basename}_{N}.npy','export_form_factor':True}

model = rpa_map_charles(N,fAlist,bA,bB,args)


x_interact_list = [['A','B'],['A','S'],['B','S']]
x0 = [chiAB,chiAS,chiBS]
interactions = create_interaction_list([],x0,x_interact_list)
#hstack fA and phip
coord = np.array(np.meshgrid(fAlist,phiPlist)).T.reshape(-1,2)

map = model.returnMap(interactions,coord,parallel = True,processes = 10)

#plot quick 
plt.figure()
phase = ['homo','macro','micro']
for i in range(3): 
    loc = np.where(map[:,-1] ==i)[0]
    if len(loc)>0:
        plt.scatter(map[loc,1],map[loc,0],s=30,zorder = 1,label = f'{phase[i]}')
plt.legend()
plt.xlabel(r'$\phi_p$')
plt.ylabel('f_A')
plt.savefig(f'./fig_map_{basename}_{N}.png')
#save map
np.save(f'./map_{basename}_{N}.npy',map)
