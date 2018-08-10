# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 12:29:22 2018

@author: YRao156839
"""

import os
import pandas as pd

def get_property_names_units():
    tables = pd.read_html('https://www.nature.com/articles/sdata201422/tables/3',
                          skiprows=0)[0]
    tables.columns = ['No', 'Property', 'Unit', 'Description']
    tables.Description=tables.Description.apply(lambda x: x.replace('\u2009',' ')) #remove\u2009 unicode space
    
    table_temp = tables[tables['Description']=='Rotational constant']
    temp = table_temp['Description'] + ' '+ table_temp['Property']
    tables.loc[tables['Description']=='Rotational constant', 'Description'] = temp
    
    tables.loc[tables['Description']=='Isotropic polarizability', 'Unit']='\\a_0^3'
    tables.loc[tables['Description']=='Electronic spatial extent', 'Unit']='\\a_0^2'
    tables.loc[tables['Description']=='Heat capacity at 298.15 K', 'Unit']='\\frac{cal}{molK}'
    
    tables['property_name:unit'] = tables['Description'] + ':' + tables['Unit']
    property_names = tables['property_name:unit'].tolist()
    return property_names
property_names_units = get_property_names_units()

def file_to_pd(file):
    line_count = 0
    molecule_dict = {}
    with open(file, 'r') as f:
        coordinate = []
        Mulliken_partial_charges = []
        for line in f:
            if line.split()=='':
                print('File %s is empty.'%file)
                break
            if line.split()==[]:
                continue
            line_count += 1
            cache = line.strip().split()
            if line_count == 1: 
                #1	Number of atoms n a
                try:
                    num_atoms = int(cache[0])
                    molecule_dict['ele_cnt'] = num_atoms
                except ValueError:
                    print('Error in 1st line of file: %s'%file)
                    break
            elif line_count == 2: 
                #2 Scalar properties (see Table 3)
                if cache[0]!='gdb':
                    print('Extraction error in file %s'%file)
                    break
                property_names_units = get_property_names_units()
                #assert len(cache) == len(property_names_units)
                molecule_dict['identifier'] = int(cache[1])
                for i in range(2, len(cache)):
                    molecule_dict[property_names_units[i]] = cache[i]
            
            elif line_count >2 and line_count < num_atoms+3: 
                #n a +3	Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
                coordinate.append(cache[0:4])
                Mulliken_partial_charges.append([cache[0], cache[4]])
            
            elif line_count == num_atoms +3:
                molecule_dict['Harmonic vibrational frequency:cm-1'] = [cache[:]]
                    
            elif line_count == num_atoms+4:
                molecule_dict['SMILE_GDB-17'] = cache[0]
                molecule_dict['SMILE_B3LYP'] = cache[1]
            elif line_count == num_atoms+5:
                molecule_dict['InChI_Corina'] = cache[0]
                molecule_dict['InChI_B3LYP'] = cache[1]
        
        molecule_dict['coordinate:Å'] = [coordinate]
        molecule_dict['Mulliken partial charges:e'] = [Mulliken_partial_charges]     
    if not molecule_dict:
        df = pd.DataFrame(molecule_dict)
        return df
    else:
        return None

files = os.listdir()
df = pd.DataFrame()
for file in files: 
    if '.xyz' in file:
        temp = file_to_pd(file)
        if temp is not None:
            df = df.append(temp)





'''
1	Number of atoms n a
2	Scalar properties (see Table 3)
3,…,n a +2	Element type, coordinate (x, y, z, in Å), Mulliken partial charges (in e) on atoms
n a +3	Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
n a +4	SMILES strings from GDB-17 and from B3LYP relaxation
n a +5	InChI strings for Corina and B3LYP geometries
'''


