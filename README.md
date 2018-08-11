# Citrine

## About

write something about 

## Example

sample input:

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

sample input description:
```
input file format:
1	Number of atoms n a
2	Scalar properties (see Table 3)
3,…,n a +2	Element type, coordinate (x, y, z, in Å), Mulliken partial charges (in e) on atoms
n a +3	Harmonic vibrational frequencies (3n a −5 or 3n a -6, in cm−1)
n a +4	SMILES strings from GDB-17 and from B3LYP relaxation
n a +5	InChI strings for Corina and B3LYP geometries
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
