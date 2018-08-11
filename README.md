# Citrine

## About

write something about 

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
```
https://www.nature.com/articles/sdata201422/tables/3
```
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
```{
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
            "units": "\\frac{cal}{molK}",
            "name": "Heat capacity at 298.15 K",
            "scalars": 6.469
        },
        {
            "units": "Ha",
            "name": "Internal energy at 0 K",
            "scalars": -40.47893
        },
        {
            "units": "Ha",
            "name": "Internal energy at 298.15 K",
            "scalars": -40.476062
        },
        {
            "units": "\\a_0^3",
            "name": "Isotropic polarizability",
            "scalars": 13.21
        },
        {
            "vectors": [
                [
                    "C",
                    -0.535689
                ],
                ...
            ],
            "units": "e",
            "name": "Mulliken partial charges"
        },
        {
            "units": "GHz",
            "name": "Rotational constant A",
            "scalars": 157.7118
        },
        {
            "units": "Ha",
            "name": "Zero point vibrational energy",
            "scalars": 0.044749
        },
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
            "units": "\u00c5",
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
}{
```
This example will serialize to the following JSON representation:

```json
{
    "category": "system.chemical",
    "chemicalFormula": "MgO2",
    "properties": {
        "units": "eV",
        "name": "Band gap",
        "scalars": [
            {
                "value": 7.8
            }
        ]
    }
}
```

# Schema

A detailed discussion of the PIF schema and usage are available at [http://citrine.io/pif](http://citrine.io/pif).
