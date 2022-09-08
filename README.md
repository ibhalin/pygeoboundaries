# pygeoboundaries
A Python client for the [geoboundaries API](https://www.geoboundaries.org/api.html), providing country political administrative boundaries.

##Installation

To do

##Access administrative boundaries

Here's a basic example which shows you how to get Mali and Senegal boudaries in a geojson file.

```python
from pygeoboundaries import get_adm

mli_sen = get_adm(['Senegal','Mali'], 'ADM0')
```

You can then use ```geopandas``` to create a GeoDataFrame.

```python
mli_sen = get_adm(['Senegal','Mali'], 'ADM0')
mli_sen
```

