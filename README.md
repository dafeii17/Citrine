# Citrine

## About

How to run the program:
1. Specify input directory, which contains all *.xyz files 
(download from [https://figshare.com/articles/Data_for_6095_constitutional_isomers_of_C7H10O2/1057646](https://figshare.com/articles/Data_for_6095_constitutional_isomers_of_C7H10O2/1057646))
2. Specify output json file path;
3. Run df_pif.py

## Example

### Sample input:

```
5
gdb 1	157.7118	157.70997	157.70699	0.	13.21	-0.3877	0.1171	0.5048	35.3641	0.044749	-40.47893	-40.476062	-40.475117	-40.498597	6.469	
C	-0.0126981359	 1.0858041578	 0.0080009958	-0.535689
H	 0.002150416	-0.0060313176	 0.0019761204	 0.133921
H	 1.0117308433	 1.4637511618	 0.0002765748	 0.133922
H	-0.540815069	 1.4475266138	-0.8766437152	 0.133923
H	-0.5238136345	 1.4379326443	 0.9063972942	 0.133923
1341.307	1341.3284	1341.365	1562.6731	1562.7453	3038.3205	3151.6034	3151.6788	3151.7078
C	C	
InChI=1S/CH4/h1H4	InChI=1S/CH4/h1H4
```

### Sample input format:
```
input file format:
1	Number of atoms n a
2	Scalar properties
3,…,n a +2	Element type, coordinate (x, y, z, in Å), Mulliken partial charges (in e) on atoms
n a +3	Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
n a +4	SMILES strings from GDB-17 and from B3LYP relaxation
n a +5	InChI strings for Corina and B3LYP geometries
```
#### Scalar properties discription:
[https://www.nature.com/articles/sdata201422/tables/3](https://www.nature.com/articles/sdata201422/tables/3).
### Sample output of conversion from File to Pandas Dataframe:
```
Pandas DataFrame columns:
Index(['Dipole moment:D', 'Electronic spatial extent:\a_0^2',
       'Energy of HOMO:Ha', 'Energy of LUMO:Ha', 'Enthalpy at 298.15 K:Ha',
       'Free energy at 298.15 K:Ha', 'Gap (ϵLUMO−ϵHOMO):Ha',
       'Harmonic vibrational frequency:cm-1',
       'Heat capacity at 298.15 K:\frac{cal}{molK}', 'InChI_B3LYP',
       'InChI_Corina', 'Internal energy at 0 K:Ha',
       'Internal energy at 298.15 K:Ha', 'Isotropic polarizability:\a_0^3',
       'Mulliken partial charges:e', 'Rotational constant A:GHz',
       'Rotational constant B:GHz', 'Rotational constant C:GHz', 'SMILE_B3LYP',
       'SMILE_GDB-17', 'Zero point vibrational energy:Ha', 'chemical_formula',
       'coordinate:Å', 'identifier'],
      dtype='object')
```
### Sample output of conversion from Pandas Dataframe to pif:
```
{
    "chemicalFormula": "C1H4",
    "category": "system.chemical",
    "properties": [
        {
            "units": "D",
            "name": "Dipole moment",
            "scalars": 0.0
        },
        ...
        {
            "vectors": [
                [
                    "C",
                    -0.0126981359,
                    1.0858041578,
                    0.0080009958
                ],
                ...
            ],
            "units": "Å",
            "name": "coordinate"
        }
    ],
    "ids": [
        {
            "name": "InChI_B3LYP",
            "value": "InChI=1S/CH4/h1H4"
        },
        ...
    ]
}
```
