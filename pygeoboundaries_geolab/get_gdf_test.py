from pygeoboundaries_geolab.pygeoboundaries import get_gdf
import geojson
import pytest
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import pdb

def test_one_country_no_md():
    gdf = get_gdf('USA')
    assert np.all(gdf.shapeGroup == 'USA')
    assert len(gdf.columns) == 6
    assert len(gdf) == 1

def test_multiple_country_no_md():
    gdf = get_gdf(['USA', 'GBR'])
    assert np.all(gdf.shapeGroup == ['USA', 'GBR'])
    assert len(gdf.columns) == 6
    assert len(gdf) == 2

def test_one_country_one_md():
    gdf = get_gdf('USA', 'Continent')
    assert np.all(gdf.shapeGroup == 'USA')
    assert np.all(gdf.Continent == 'Northern America')
    assert len(gdf.columns) == 7
    assert len(gdf) == 1

def test_one_country_multiple_md():
    gdf = get_gdf('USA', ['Continent', 'worldBankIncomeGroup'])
    assert np.all(gdf.shapeGroup == 'USA')
    assert np.all(gdf.Continent == 'Northern America')
    assert np.all(gdf['worldBankIncomeGroup'] == 'High-income Countries')
    assert len(gdf.columns) == 8
    assert len(gdf) == 1

def test_multiple_country_one_md():
    gdf = get_gdf(["SEN", 'MLI'], 'Continent')
    assert np.all(gdf.shapeGroup == ['SEN', 'MLI'])
    assert np.all(gdf.Continent == 'Africa')
    assert len(gdf.columns) == 7

    gdf = get_gdf(['USA', 'ABW', 'TKL'], 'Continent')
    assert np.all(gdf.shapeGroup == ['USA', 'ABW', 'TKL'])
    assert np.all(gdf.Continent == ['Northern America', 'Latin America and the Caribbean', 'Oceania'])
    assert np.all(gdf.loc[gdf['shapeGroup'] == 'ABW', 'Continent'] == 'Latin America and the Caribbean')
    assert len(gdf.columns) == 7

def test_multiple_country_multiple_md():
    gdf = get_gdf(['FSM', 'Jordan', 'GNQ'], ['UNSDG-subregion', 'Continent'])
    assert np.all(gdf.shapeGroup == ['FSM', 'JOR', 'GNQ'])
    assert np.all(gdf['UNSDG-subregion'] == ["Micronesia", 'Western Asia', 'Middle Africa'])
    assert np.all(gdf.Continent == ['Oceania', 'Asia', 'Africa'])
    assert len(gdf.columns) == 8
    assert len(gdf) == 3

def test_country_name_conversion():
    gdf = get_gdf(["SEN", 'mali'], 'Continent')
    assert np.all(gdf.shapeGroup == ['SEN', 'MLI'])
    assert np.all(gdf.Continent == 'Africa')

def test_all_no_md():
    gdf = get_gdf('ALL')
    assert len(gdf.columns) == 6
    assert len(gdf) == 230 # current num of territories as of April 2025

def test_all_one_md():
    gdf = get_gdf('ALL', 'Continent')
    assert len(gdf.columns) == 7
    assert len(gdf) == 230 # current num of territories as of April 2025
    assert len(gdf[gdf.Continent == 'Undefined']) == 0

def test_all_multiple_md():
    gdf = get_gdf('ALL', ['worldBankIncomeGroup', 'UNSDG-subregion'])
    assert len(gdf.columns) == 8
    assert len(gdf) == 230 # current num of territories as of April 2025
    assert len(gdf[gdf['UNSDG-subregion'] == 'Undefined']) == 0
    assert set(gdf.worldBankIncomeGroup) == set(['High-income Countries', 
                                                 'Low-income Countries',
                                                 'Lower-middle-income Countries',
                                                 'No income group available',
                                                 'Upper-middle-income Countries'])

def test_coord_location():
    gdf = get_gdf('ALL')

    dhaka = Point(90.38749998918445, 23.712500002650515)
    containing_country = gdf[gdf.geometry.contains(dhaka)]
    assert len(containing_country) == 1
    country_name = containing_country.iloc[0].shapeName
    assert country_name == 'Bangladesh'

    manhattan = Point(-73.9822, 40.7685)
    containing_country = gdf[gdf.geometry.contains(manhattan)]
    assert len(containing_country) == 1
    country_name = containing_country.iloc[0].shapeName
    assert country_name == 'United States'

    pacific_ocean = Point(-152.478, 36.512)
    containing_country = gdf[gdf.geometry.contains(pacific_ocean)]
    assert len(containing_country) == 0
