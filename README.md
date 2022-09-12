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

You can pass a list into ```territory``` to retreive multiple countries' data

```python
mli_sen = get_adm(['Senegal', 'Mali'], adm='ADM0')
```

You can then use ```geopandas``` to create a GeoDataFrame with the geojson you just got.

```python
import geopandas as gpd
gdf = gpd.GeoDataFrame.from_features(mli_sen)
```

Or plot it directly with ```folium``` or any other mapping tool.

```python
m = folium.Map(location=[15.3610,-5.5178], zoom_start=6)
folium.GeoJson(mli_sen).add_to(m)
```

![Senegal and Mali's ADM1 boundaries](https://i.ibb.co/hmyY5V6/mali-sen.png)

Allowed values for ```territory```: 
* ISO 3166-1 ([alpha3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)) : AFG, QAT, YEM, etc.
* ISO 3166-1 ([alpha2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) : AF, QA, YE, etc.
* Country name in any of the following languages : Arabic, Armenian, Basque, Bulgarian, Chinese (simplified), Chinese (traditional), Czech, Danish, Dutch, English, Esperanto, Estonian, Finnish, French, German, Greek, Hungarian, Italian, Japanese, Korean, Lithuanian, Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Spanish, Swedish, Thai, Ukrainian.

For more information, check out https://stefangabos.github.io/world_countries/ (the data source for ISO codes and countries names)
    
Allowed format for```territory```:
* a single string : "Senegal", "SEN", "เซเนกัล" 
* a list of strings : ["SEN", "Mali'], ["セネガル", "մալի"]

Allowed values for ```adm```:
* 'ADM0' to 'ADM5' (if exists for specified country)
* int 0 to 5
* int -1 (returns the smallest available ADM level)
For more information about ADM levels, check out https://www.geoboundaries.org/index.html
