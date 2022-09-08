# pygeoboundaries
A Python client for the [geoboundaries API](https://www.geoboundaries.org/api.html), providing country political administrative boundaries.

## Installation

To do

## Access administrative boundaries

Here's a basic example which shows you how to get Senegal boudaries in a geojson file.

```python
from pygeoboundaries import get_adm

sen = get_adm(territory='Senegal', adm='ADM0')
```

You can pass a list into the ```territory``` argument to retreive multiple countries' data

```python
mli_sen = get_adm(['Senegal', 'Mali'], adm='ADM0')
```

Allowed values for the ```territory``` argument : 
* ISO 3166-1 ([alpha3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)) : AFG, QAT, YEM, etc.
* ISO 3166-1 ([alpha2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) : AF, QA, YE, etc.
* Country name in any of the following languages : Arabic, Armenian, Basque, Bulgarian, Chinese (simplified), Chinese (traditional), Czech,Danish, Dutch, English, Es peranto, Estonian, Finnish, French, German, Greek, Hungarian, Italian, Japanese, Korean, Lithuanian, Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Spanish, Swedish, Thai, Ukrainian.
For more information, check out https://stefangabos.github.io/world_countries/ (the data source for ISO codes and countries names)
    
Allowed format for the ```territory``` argument :
* a single string : "Senegal", "SEN", "เซเนกัล" 
* a list of strings : ["SEN", "Mali'], ["セネガル", "մալի"]

Allowed values for the <adm> argument :
* 'ADM0' to 'ADM5' (if exists for specified country)
* int 0 to 5
* int -1 (returns the smallest available ADM level)
For more information about ADM levels, check out https://www.geoboundaries.org/index.html

<!-- You can then use ```geopandas``` to create a GeoDataFrame with the geojson you just got.

```python
import geopandas as gpd
#TO DO : gpd stuff and plotting
```
 -->



