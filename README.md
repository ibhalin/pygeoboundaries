# pygeoboundaries_geolab
A Python client for the [geoboundaries API](https://www.geoboundaries.org/api.html), providing country political administrative boundaries.

## Installation

`pip install pygeoboundaries-geolab`

## Access administrative boundaries

Here's a basic example which shows you how to get Senegal boundaries in a geojson file.

```python
from pygeoboundaries_geolab import get_adm

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
* ISO 3166-1 ([alpha3](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-3)) : AFG, QAT, YEM, etc. (⭐️ recommended approach)
* ISO 3166-1 ([alpha2](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)) : AF, QA, YE, etc.
* Country name in any of the following languages : Arabic, Armenian, Basque, Bulgarian, Chinese (simplified), Chinese (traditional), Czech, Danish, Dutch, English, Esperanto, Estonian, Finnish, French, German, Greek, Hungarian, Italian, Japanese, Korean, Lithuanian, Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Spanish, Swedish, Thai, Ukrainian. (🙋 out of date, need help supporting)
* 'ALL' to get boundaries for all available countries

For more information, check out https://stefangabos.github.io/world_countries/ (the data source for ISO codes and countries names)
    
Allowed format for ```territory```:
* a single string : "Senegal", "SEN", "เซเนกัล", 'ALL'
* a list of strings : ["SEN", 'Mali'], ["セネガル", "մալի"]

Allowed values for ```adm```:
* 'ADM0' to 'ADM5' (if exists for specified country)
* int 0 to 5
* int -1 (returns the smallest available ADM level)
For more information about ADM levels, check out https://www.geoboundaries.org/index.html

## Access country metadata

```python
from pygeoboundaries_geolab import get_gdf
gdf = get_gdf(['FSM', 'Jordan', 'GNQ'], ['UNSDG-subregion', 'Continent'])
```

This will return the following geopandas GeoDataFrame `gdf` with geometry and requested metadata for the Federated States of Micronesia, Jordan, and Equatorial Guinea:

```
                                            geometry                        shapeName shapeISO                  shapeID shapeGroup shapeType UNSDG-subregion Continent
0  MULTIPOLYGON (((154.7806 1.02662, 154.78042 1....   Federated States of Micronesia      FSM  75748993B60512971346220        FSM      ADM0      Micronesia   Oceania
1  POLYGON ((39.07694 32.33079, 39.06063 32.3343,...  the Hashemite Kingdom of Jordan      JOR  64752131B76849546124065        JOR      ADM0    Western Asia      Asia
2  MULTIPOLYGON (((5.63304 -1.40378, 5.63046 -1.4...                Equatorial Guinea      GNQ  36962785B17032204434992        GNQ      ADM0   Middle Africa    Africa
```

'shapeGroup' is better to use than 'shapeISO', as all entries/countries will have a 'shapeGroup' but not necessarily 'shapeISO'.

You can request any of the following metadata fields for each country:
- 'boundaryID'
- 'boundaryName'
- 'boundaryISO'
- 'boundaryYearRepresented'
- 'boundaryType' (ADM level)
- 'boundaryCanonical'
- 'boundarySource'
- 'boundaryLicense'
- 'licenseDetail'
- 'licenseSource'
- 'boundarySourceURL'
- 'sourceDataUpdateDate'
- 'buildDate'
- 'Continent'
- 'UNSDG-region' (more info: https://unstats.un.org/sdgs/indicators/regional-groups/)
- 'UNSDG-subregion' (more info: https://unstats.un.org/sdgs/indicators/regional-groups/)
- 'worldBankIncomeGroup'
- 'admUnitCount'
- 'meanVertices'
- 'minVertices'
- 'maxVertices'
- 'meanPerimeterLengthKM'
- 'minPerimeterLengthKM'
- 'maxPerimeterLengthKM'
- 'meanAreaSqKM'
- 'minAreaSqKM'
- 'maxAreaSqKM'
- 'staticDownloadLink'
- 'gjDownloadURL'
- 'tjDownloadURL'
- 'imagePreview'
- 'simplifiedGeometryGeoJSON'

## Testing

Run `pytest` in the terminal
