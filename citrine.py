# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 12:29:22 2018

@author: YRao156839
"""

import os
import pandas as pd
from collections import Counter
from pypif import pif
from pypif.obj import *


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

def file_to_pd(file, path, property_names_units):
    line_count = 0
    molecule_dict = {}
    with open(file, 'r') as f:
        coordinate = []
        Mulliken_partial_charges = []
        atoms = []
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
                    molecule_dict[property_names_units[i]] = float(cache[i])
            
            elif line_count >2 and line_count < num_atoms+3: 
                #n a +3	Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
                atoms.append(cache[0])
                coord = [float(i) for i in cache[1:4]]
                coordinate.append([cache[0], coord[0], coord[1], coord[2]])
                Mulliken_partial_charges.append([cache[0], float(cache[4])])
            
            elif line_count == num_atoms +3:
                molecule_dict['Harmonic vibrational frequency:cm-1'] = [[float(i) for i in cache]]
                    
            elif line_count == num_atoms+4:
                molecule_dict['SMILE_GDB-17'] = cache[0]
                molecule_dict['SMILE_B3LYP'] = cache[1]
            elif line_count == num_atoms+5:
                molecule_dict['InChI_Corina'] = cache[0]
                molecule_dict['InChI_B3LYP'] = cache[1]
        
        chemical_formula = ''
        for key, value in sorted(Counter(atoms).items()):
            chemical_formula += str(key)+str(value)
        molecule_dict['chemical_formula'] = chemical_formula
        molecule_dict['coordinate:Å'] = [coordinate]
        molecule_dict['Mulliken partial charges:e'] = [Mulliken_partial_charges] 
        
    if molecule_dict:
        df = pd.DataFrame(molecule_dict)
        return df
    else:
        return None

def pd_to_pifmat(df):
    chemical_system = ChemicalSystem()
    df_formula = df.chemical_formula
    chemical_system.chemical_formula = str(df_formula.values[0])
    
    df_id = df[['InChI_B3LYP', 'InChI_Corina','SMILE_B3LYP','SMILE_GDB-17', 'identifier']]
    label_ids = []
    for i in range(len(df_id.columns)):
        label_ids.append(Id())
        label_ids[i].name = df_id.columns[i]
        label_ids[i].value = str(df_id[df_id.columns[i]].values[0])
    chemical_system.ids = label_ids
    
    df.drop(columns=['InChI_B3LYP', 'InChI_Corina','SMILE_B3LYP','SMILE_GDB-17',
                     'identifier', 'chemical_formula'], inplace=True)
    properties=[]
    names_units = [i.split(':') for i in df.columns]
    for i in range(len(df.columns)):
        properties.append(Property())
        properties[i].name = names_units[i][0]
        properties[i].units = names_units[i][1]
        if df.columns[i]=='Mulliken partial charges:e' or df.columns[i]=='coordinate:Å':
            properties[i].vectors = df[df.columns[i]].values[0]
        else:
            properties[i].scalars = df[df.columns[i]].values[0]
    chemical_system.properties = properties
    return chemical_system

def main():
    path = os.getcwd()
    property_names_units = get_property_names_units()
    files = os.listdir('./input')
    f = open('./output/test.json', 'w')
    for file in files: 
        if '.xyz' in file:
            df = file_to_pd(file, path, property_names_units)
            if df is not None:
               chemical_system = pd_to_pifmat(df)
               pif.dump(chemical_system, f, indent=4)
    f.close()

if __name__ == '__main__':
    main()



'''
1	Number of atoms n a
2	Scalar properties (see Table 3)
3,…,n a +2	Element type, coordinate (x, y, z, in Å), Mulliken partial charges (in e) on atoms
n a +3	Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
n a +4	SMILES strings from GDB-17 and from B3LYP relaxation
n a +5	InChI strings for Corina and B3LYP geometries
'''


