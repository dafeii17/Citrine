# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 12:29:22 2018

@author: YingliRao
"""

import os
import argparse
import pandas as pd
from collections import Counter
from pypif import pif
from pypif.obj import *

def get_property_names_units():
    '''
    extract properties name and unit from description table
    property name = Description column from table
    '''
    tables = pd.read_html('https://www.nature.com/articles/sdata201422/tables/3',
                          skiprows=0)[0]
    tables.columns = ['No', 'Property', 'Unit', 'Description']
    tables.Description=tables.Description.apply(lambda x: x.replace('\u2009',' ')) #remove\u2009 unicode space
    
    #differentiate three Rotational constant by adding property column A, B, C 
    table_temp = tables[tables['Description']=='Rotational constant']
    temp = table_temp['Description'] + ' '+ table_temp['Property']
    tables.loc[tables['Description']=='Rotational constant', 'Description'] = temp
    
    #latex format some units_superscript_subscript
    tables.loc[tables['Description']=='Isotropic polarizability', 'Unit']='\\a_0^3'
    tables.loc[tables['Description']=='Electronic spatial extent', 'Unit']='\\a_0^2'
    tables.loc[tables['Description']=='Heat capacity at 298.15 K', 'Unit']='\\frac{cal}{molK}'
    
    #property names and unit are combined together 'name:unit'
    tables['property_name:unit'] = tables['Description'] + ':' + tables['Unit']
    property_names_units = tables['property_name:unit'].tolist()
    return property_names_units

def file_to_pd(file, path, property_names_units):
    '''
    input file format:
    1	Number of atoms n a
    2	Scalar properties (see Table 3)
    3,…,n a +2	Element type, coordinate (x, y, z, in Å), Mulliken partial charges (in e) on atoms
    n a +3	Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
    n a +4	SMILES strings from GDB-17 and from B3LYP relaxation
    n a +5	InChI strings for Corina and B3LYP geometries
    '''
    line_count = 0
    molecule_dict = {}
    with open(os.path.join(path, file), 'r') as f:
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
            if line_count == 1:  # 1st line Number of atoms n a
                try:
                    num_atoms = int(cache[0])
                except ValueError:
                    print('Error in 1st line of file: %s'%file)
                    break
            elif line_count == 2:  #2nd line Scalar properties (see Table 3)
                property_names_units = get_property_names_units()
                try:
                    assert len(cache) == len(property_names_units)
                except AssertionError: 
                    print('Error in 2nd line of file: %s'%file)
                    break
                molecule_dict['identifier'] = int(cache[1])
                for i in range(2, len(cache)):
                    molecule_dict[property_names_units[i]] = float(cache[i])
            
            elif line_count >2 and line_count < num_atoms+3: 
                '''
                #line 3 to num_atoms+2: 
                    Element type, coordinate (x, y, z, in Å), 
                    Mulliken partial charges (in e) on atoms
                '''
                atoms.append(cache[0]) 
                coord = [float(i) for i in cache[1:4]]
                coordinate.append([cache[0], coord[0], coord[1], coord[2]])
                Mulliken_partial_charges.append([cache[0], float(cache[4])])
            
            elif line_count == num_atoms +3:
                #line num_atoms+3: Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
                molecule_dict['Harmonic vibrational frequency:cm-1'] = [[float(i) for i in cache]]
                    
            elif line_count == num_atoms+4:
                #line num_atoms +4	SMILES strings from GDB-17 and from B3LYP relaxation
                molecule_dict['SMILE_GDB-17'] = cache[0]
                molecule_dict['SMILE_B3LYP'] = cache[1]
            elif line_count == num_atoms+5:
                #line num_atoms +5	InChI strings for Corina and B3LYP geometries
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
    
    #chemical formula attribute
    df_formula = df.chemical_formula
    chemical_system.chemical_formula = str(df_formula.values[0])
    
    #ids attribute
    df_id = df[['InChI_B3LYP', 'InChI_Corina','SMILE_B3LYP','SMILE_GDB-17', 'identifier']]
    label_ids = []
    for i in range(len(df_id.columns)):
        label_ids.append(Id())
        label_ids[i].name = df_id.columns[i]
        label_ids[i].value = str(df_id[df_id.columns[i]].values[0])
    chemical_system.ids = label_ids

    #properties attribute
    df.drop(columns=['InChI_B3LYP', 'InChI_Corina','SMILE_B3LYP','SMILE_GDB-17',
                    'identifier', 'chemical_formula'], inplace=True)
    properties=[]
    names_units = [i.split(':') for i in df.columns] #df.columns are property_names_units, separate name and unit
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
    property_names_units = get_property_names_units()
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file_dir", type=str, required=True,
                    help="the input file directory")
    parser.add_argument("--output_json_path", type=str, required=True,
                    help="the output json file path")
    args = parser.parse_args()
    input_path = args.input_file_dir
    output_path = args.output_json_path
    files = os.listdir(input_path)
    f = open(output_path, 'w')
    num = 0
    for file in files: #convert each file to pd.DataFrame then output with pif
        if '.xyz' in file: 
            df = file_to_pd(file, input_path, property_names_units)
            if df is not None:
               chemical_system = pd_to_pifmat(df)
               pif.dump(chemical_system, f, indent=4)
               num += 1
               if num % 5 == 0:
                   print('%d files have been processed'%num)
    print('In total %d files have been processed'%num)
    f.close()

if __name__ == '__main__':
    main()






