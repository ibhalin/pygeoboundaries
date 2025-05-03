from distutils.core import setup
setup(name='pygeoboundaries_geolab',
      version='0.0.2',
      packages=['pygeoboundaries_geolab'],
      install_requires=['geojson', 'requests_cache', 'geopandas', 'shapely', 'pytest', 'numpy']
      )
