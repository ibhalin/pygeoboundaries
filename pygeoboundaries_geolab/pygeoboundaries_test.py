from pygeoboundaries_geolab.pygeoboundaries import _validate_adm, _get_iso3_from_name_or_iso2, get_adm, get_gdf
import geojson
import pytest
import geopandas as gpd
from shapely.geometry import Point

def test_validate_adm():
    assert _validate_adm(1) == 'ADM1'
    assert _validate_adm(5) == 'ADM5'
    assert _validate_adm('2') == 'ADM2'
    assert _validate_adm('3') == 'ADM3'
    assert _validate_adm('all') == 'ALL'
    assert _validate_adm('adm1') == 'ADM1'
    assert _validate_adm('ADM2') == 'ADM2'
    assert _validate_adm('aDm3') == 'ADM3'

def test_get_iso3_from_name():
    countries = {
        'ألبانيا' : 'Albanie',
        'Բահրեյն' : 'Bahrein',
        'Arabiar Emirerri Batuak': 'EAU',
        'Бразилия': 'Brazil',
        '古巴': 'Cuba',
        '賽普勒斯': 'Cyprus',
        'Džibutsko': 'Djibouti',
        'Elfenbenskysten': 'Ivory Coast',
        'Equatoriaal-Guinea' : 'Guinee equa',
        'Fiji': 'Fiji',
        'Filipinoj': 'Philipinnes',
        'Gruusia': 'Georgie',
        'Intia': 'Inde',
        'Irlande' : 'Irlande',
        'Jemen': 'Yemen',
        'Ιαπωνία': 'Japan',
        'Kamerun': 'Cameroun',
        'Kazakistan' : 'Kazakstan',
        'ガンビア': 'Gambie',
        '키르기스스탄': 'kiribati',
        'Kolumbija': 'Colombie',
        'Litauen': 'Lituanie',
        'Luksemburg': 'LUX',
        'Madagáscar': 'Mada',
        'Mexic': 'MEX',
        'Монако': 'Monaco',
        'Nový Zéland': 'New Zealand',
        'Papúa Nueva Guinea': 'Papouasie',
        'Ryssland': 'Russie',
        'อุรุกวัย': 'Uruguay',
        'Шрі-Ланка': 'Sri Lanka'
    }
    for k,v in countries.items():
        print(_get_iso3_from_name_or_iso2(k))
        assert len(_get_iso3_from_name_or_iso2(k)) == 3

def test_get_adm():
    assert type(get_adm('sn','ADM0')) == geojson.feature.FeatureCollection
    assert type(get_adm('Senegal','ADM0')) == geojson.feature.FeatureCollection
    for i in range(6):
        assert type(get_adm('France',i)) == geojson.feature.FeatureCollection
    assert type(get_adm('Vanuatu',-1)) == geojson.feature.FeatureCollection
