"""Runfola, Daniel, Community Contributors, and [v4.0: Lindsey Rogers, Joshua Habib, Sidonie Horn, Sean Murphy, Dorian Miller, Hadley Day, Lydia Troup, Dominic Fornatora, Natalie Spage, Kristina Pupkiewicz, Michael Roth, Carolina Rivera, Charlie Altman, Isabel Schruer, Tara McLaughlin, Russ Biddle, Renee Ritchey, Emily Topness, James Turner, Sam Updike, Helena Buckman, Neel Simpson, Jason Lin], [v2.0: Austin Anderson, Heather Baier, Matt Crittenden, Elizabeth Dowker, Sydney Fuhrig, Seth Goodman, Grace Grimsley, Rachel Layko, Graham Melville, Maddy Mulder, Rachel Oberman, Joshua Panganiban, Andrew Peck, Leigh Seitz, Sylvia Shea, Hannah Slevin, Rebecca Yougerman, Lauren Hobbs]. "geoBoundaries: A global database of political administrative boundaries." Plos one 15, no. 4 (2020): e0231866."""

from typing import List, Optional
import geojson
import requests
from . import countries_iso_dict
from . import iso_codes
from requests_cache import CachedSession
import geopandas as gpd
import pdb

_session = CachedSession(expire_after=604800) #cache expires after 1 week

def clear_cache():
    _session.cache.clear()

def set_cache_expire_time(seconds: int):
    """Update cache expiring time. Does not clear cache."""
    global _session
    _session = CachedSession(expire_after=seconds)

def disable_cache():
    global _session
    _session = requests

def _is_valid_adm(iso3, adm: str) -> bool :
    html = _session.get("https://www.geoboundaries.org/api/current/gbOpen/{}/".format(iso3), verify=True).text
    #print('adm in html =' + str(adm in html))
    return adm in html

def _validate_adm(adm: str | int) -> str :
    if type(adm).__name__ == 'int' or len(str(adm)) == 1:
        adm = 'ADM' + str(adm)
    if str.upper(adm) in ['ADM{}'.format(str(i)) for i in range(6)] or str.upper(adm) == 'ALL':
        return str.upper(adm)
    raise KeyError

def _get_smallest_adm(iso3):
    current_adm = 5
    adm_exists = False
    while current_adm >= 0:
        #print('testing adm'+str(current_adm))
        if _is_valid_adm(iso3, 'ADM' + str(current_adm)):
            break
        current_adm -= 1 
    print('Smallest ADM level found for {} : ADM{}'.format(iso3, current_adm))
    return 'ADM' + str(current_adm)

def _is_valid_iso3_code(territory: str) -> bool :
    return str.lower(territory) in iso_codes.iso_codes

def _get_iso3_from_name_or_iso2(name: str) -> str:
    if str.upper(name) == 'ALL':
        return 'ALL'
    try :
        return str.upper(countries_iso_dict.countries_iso3[str.lower(name)])
    except KeyError as e:
        print("KeyError : Couldn't find country named {}".format(e))
        raise KeyError

def _generate_url(territory: str, adm : str | int) -> str :
    iso3 = str.upper(territory) if _is_valid_iso3_code(territory) else _get_iso3_from_name_or_iso2(territory)
    if adm != -1:
        adm = _validate_adm(adm)
    else:
        adm = _get_smallest_adm(iso3)
    if not (iso3 == 'ALL' or _is_valid_adm(iso3, adm)):
        print("KeyError : ADM level '{}' doesn't exist for country '{}' ({})".format(adm, territory, iso3))
        raise KeyError
    return "https://www.geoboundaries.org/api/current/gbOpen/{}/{}/".format(iso3, adm)

def get_metadata(territory: str, adm: str | int) -> dict:
    """
    Returns a json of specifided territory's metadata.
    Use territory='ALL' to get metadata for all territories.
    Use adm='ALL' to get metadata for every ADM levels.
    """
    cached_response = _session.get(_generate_url(territory, adm), verify=True).json()
    return cached_response #TO DO get rid of verify arg

def _get_data(territory: str, adm: str, simplified: bool) -> dict:
    """Requests the geoboundaries API and returns a JSON str object of the specified territory and ADM """
    geom_complexity = 'simplifiedGeometryGeoJSON' if simplified else 'gjDownloadURL'
    try:
        json_uri = get_metadata(territory, adm)[geom_complexity]
    except:
        print("Error while requesting geoboudaries API\n URL : {}\n".format(_generate_url(territory, adm)))
        raise
    return _session.get(json_uri).text

def get_adm(territories: str | List[str], 
            adm: str | int, 
            simplified: bool = True) -> dict:
    """
    Returns a json of specifided territories at specifided adm levels.

    Allowed values for <territories> argument : 

        - ISO 3166-1 (alpha2) : AFG, QAT, YEM, etc.
        - ISO 3166-1 (alpha3) : AF, QA, YE, etc.
        - Country name (i.e ADM0 territories) in any of the following languages : Arabic, Armenian, Basque, Bulgarian, Chinese (simplified), Chinese (traditional), Czech,
             Danish, Dutch, English, Esperanto, Estonian, Finnish, French, German, Greek, Hungarian, Italian, Japanese, Korean, Lithuanian,
             Norwegian, Polish, Portuguese, Romanian, Russian, Slovak, Spanish, Swedish, Thai, Ukrainian
        For more information, check out https://stefangabos.github.io/world_countries/ (the data source for ISO codes and countries' names)
    
    Allowed format for <territories> argument :

        - a single string : "Senegal", "SEN", "เซเนกัล" , 'ALL'
        - a list of strings : ["SEN", "Mali'], ["セネガル", "մալի"]

    Allowed values for <adm> argument :

        - 'ADM0' to 'ADM5' (if exists for specified country)
        - int 0 to 5
        - int -1 (returns the smallest available ADM level)
        For more information about ADM levels, check out https://www.geoboundaries.org/index.html
    """

    if territories == 'ALL':
        md = get_metadata('ALL', adm)
        territories = [country['boundaryISO'] for country in md]
        # TODO: optimize by not doing a second API call for each country
    
    if type(territories) == str:
        gjson = geojson.loads(_get_data(territories, adm, simplified))['features'][0]
        gjson = _correct_properties(gjson)
        return geojson.FeatureCollection(gjson)
    geojsons = [_correct_properties(geojson.loads(_get_data(i, adm, simplified))['features'][0]) for i in territories]
    feature_collection = geojson.FeatureCollection(geojsons)
    return feature_collection

def _correct_properties(gjson: geojson.feature.Feature) -> geojson.feature.Feature:
    territory = gjson.properties['shapeGroup']

    # Bangladesh
    if territory == 'BGD':
        gjson.properties['shapeName'] = 'Bangladesh'

    return gjson

def _correct_metadata(territory, metadata, metadata_fields):
    '''
    Bespoke corrections for countries with known issues; there are likely many more.
    '''
    
    # Antarctica
    if territory == 'ATA':
        if 'Continent' in metadata_fields: metadata['Continent'] = 'Antarctica'
        if 'UNSDG-region' in metadata_fields: metadata['UNSDG-region'] = 'Antarctica'
        if 'UNSDG-subregion' in metadata_fields: metadata['UNSDG-subregion'] = 'Antarctica'
        if 'worldBankIncomeGroup' in metadata_fields: metadata['worldBankIncomeGroup'] = 'No income group available'

    # Bermuda
    if territory == 'BMU':
        if 'UNSDG-subregion' in metadata_fields: metadata['UNSDG-subregion'] = 'Northern America'

    # Canada
    if territory == 'CAN':
        if 'UNSDG-subregion' in metadata_fields: metadata['UNSDG-subregion'] = 'Northern America'

    # Greenland
    if territory == 'GRL':
        if 'UNSDG-subregion' in metadata_fields: metadata['UNSDG-subregion'] = 'Northern America'

    # United States
    if territory == 'USA':
        if 'UNSDG-subregion' in metadata_fields: metadata['UNSDG-subregion'] = 'Northern America'

    # Guernsey
    if territory == 'GGY':
        # https://databank.worldbank.org/metadataglossary/jobs/country/CHI
        if 'worldBankIncomeGroup' in metadata_fields: metadata['worldBankIncomeGroup'] = 'High-income Countries'

    # Pitcairn Island
    if territory == 'PCN':
        if 'worldBankIncomeGroup' in metadata_fields: metadata['worldBankIncomeGroup'] = 'No income group available'

    # Kosovo
    if territory == 'XKX':
        # https://data.worldbank.org/country/kosovo
        if 'worldBankIncomeGroup' in metadata_fields: metadata['worldBankIncomeGroup'] = 'Upper-middle-income Countries'

    return metadata

def get_gdf(territories: str | List[str], 
            metadata_fields: Optional[str | List[str]] = None, 
            apply_metadata_corrections: bool = True,
            simplified: bool = True) -> gpd.geodataframe.GeoDataFrame:
    '''
    Returns a geopandas GeoDataFrame containing the requested territory geometry
    (polygons) as well as columns for the other requested metadata fields. Default
    columns included in the dataframe are 'geometry', 'shapeName' (country name),
    'shapeISO', 'shapeID', 'shapeGroup', and 'shapeType' (ADM level).

    Allowed values for <metadata_fields> argument, it can be a
    single of the following strings or a list of these strings: 

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
    '''
    
    # TODO: optimize by capturing all metadata with get_adm so that we don't
    # have to do a second request for each country

    if not (type(territories) == str and str.upper(territories) == 'ALL'):
        if type(territories) == str:
            territories = [territories]
        for i, territory in enumerate(territories):
            territories[i] = str.upper(territory) if _is_valid_iso3_code(territory) else _get_iso3_from_name_or_iso2(territory)

    adm = 'ADM0' # TODO: support other ADM levels
    feature_collection = get_adm(territories, adm, simplified)
    gdf = gpd.GeoDataFrame.from_features(feature_collection)

    # pg. 3 of (Daniel Runfola et al. “geoBoundaries: A global database of political ad-
    # ministrative boundaries”. In: PloS one 15.4 (2020), e0231866.) indicates the CRS
    # is WGS-84, but it is never made explicitly clear
    gdf = gdf.set_crs('WGS84')

    if metadata_fields:
        if type(metadata_fields) == str:
            metadata_fields = [metadata_fields]
        for md_field in metadata_fields:
            gdf[md_field] = None
        for territory in gdf.shapeGroup:
            md = get_metadata(territory, adm)
            if apply_metadata_corrections:
                md = _correct_metadata(territory, md, metadata_fields)
            for md_field in metadata_fields:
                gdf.loc[gdf['shapeGroup'] == territory, md_field] = md[md_field]
    
    return gdf
