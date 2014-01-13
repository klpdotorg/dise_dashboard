import re

from django.utils import simplejson as json
from django.contrib.gis.geos import Polygon
from geojson import Feature, FeatureCollection, Point, dumps as geojson_dumps

from schools.olap_models import get_models

class BaseEntity:
    @classmethod
    def to_json_str(cls, d=dict()):
        return json.dumps(d)

    @classmethod
    def to_geojson_str(cls, d=dict()):
        return geojson_dumps(d)

    @classmethod
    def getInfo(cls, params):
        # this just parses the dictionary from _getinfo and returns JSON
        result = cls()._getinfo(params)
        return cls.to_geojson_str(result)

    @classmethod
    def search(cls, params):
        # this just parses the dictionary from _search() and returns JSON
        result = cls()._search(params)
        return cls.to_geojson_str(result)


    @classmethod
    def getSchools(cls, params):
        # this just parses the dictionary from _getschools() and returns JSON
        result = cls()._getschools(params)
        return cls.to_geojson_str(result)


class School(BaseEntity):
    # For methods that start with `School`
    def _getinfo(self, params):
        # gets the details of a school and returns a dictionary
        code = params.get('code', -1)
        result = dict()
        result['query'] = params

        try:
            SchoolModel = get_models(params.get('session', '10-11'), 'school')
            school = SchoolModel.objects.get(school_code__iexact=code)

            result['school'] = self._get_geojson(school)
        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _get_geojson(self, school):
        # returns a geojson feature for the given DiseFFTTBasicData object.
        # FFTT = sesstion from/to. for 2010-11: 1011
        return Feature(
            geometry=Point(
                [school.centroid.x, school.centroid.y] if school.centroid is not None else []
            ),
            properties={
                'name': school.school_name,
                'cluster_name': school.cluster_name,
                'block_name': school.block_name,
                'district': school.district,
                'popupContent': ', '.join([school.school_name, school.cluster_name])
            },
            id=school.school_code
        )

    def _search(self, params):
        # This seaches all the base models, depending on the session and retuns list of schools
        result = dict()
        result['query'] = params
        SchoolModel = get_models(params.get('session', '10-11'), 'school')

        if len(params.keys()) > 1:
            schools = SchoolModel.objects.filter(centroid__isnull=False)

        if 'name' in params and params.get('name', ''):
            schools = schools.filter(school_name__icontains=params.get('name'))

        if 'cluster' in params and params.get('cluster', ''):
            schools = schools.filter(cluster_name__icontains=params.get('cluster'))

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73974609375,12.5223906020692,79.4476318359375,13.424352095715332"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                schools = schools.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            schools = schools[:params.get('limit')]

        # print schools.query
        temp_l = []
        for sch in schools:
            temp_l.append(self._get_geojson(sch))
        result['schools'] = FeatureCollection(temp_l)
        return result


class Cluster(BaseEntity):
    # For all methods that start with Cluster
    def _getschools(self, params):
        # returns list of schools in a given cluster
        # if format = geo, returns FeatureCollection
        # if format = plain, returns a plain list
        name = params.get('name')
        result = dict()
        result['query'] = params

        try:
            SchoolModel = get_models(params.get('session', '10-11'), 'school')

            temp_l = []
            school_api = School()
            schools = SchoolModel.objects.filter(
                cluster_name__iexact=name,
                # NOTE: Not sending schools without centroid
                # because there is no way to show them
                centroid__isnull=False
            )
            for sch in schools:
                temp_l.append(school_api._get_geojson(sch))
            result['schools'] = FeatureCollection(temp_l)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _get_geojson(self, cluster):
        # returns a geojson feature for the given DiseFFTTBasicData object.
        # FFTT = sesstion from/to. for 2010-11: 1011
        return Feature(
            geometry=Point(
                [cluster.centroid.x, cluster.centroid.y] if cluster.centroid is not None else []
            ),
            properties={
                'cluster_name': cluster.cluster_name,
                'block_name': cluster.block_name,
                'district': cluster.district,
                'popupContent': ', '.join([cluster.cluster_name, cluster.block_name])
            },
            id=cluster.cluster_name
        )

    def _search(self, params):
        # searches clusters and returns list
        result = dict()
        result['query'] = params
        ClusterModel = get_models(params.get('session', '10-11'), 'cluster')

        clusters = ClusterModel.objects.filter(centroid__isnull=False)

        if 'name' in params and params.get('name', ''):
            clusters = clusters.filter(cluster_name__icontains=params.get('name'))

        if 'block' in params and params.get('block', ''):
            clusters = clusters.filter(block_name__icontains=params.get('block'))

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73974609375,12.5223906020692,79.4476318359375,13.424352095715332"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                clusters = clusters.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            clusters = clusters[:params.get('limit')]

        print clusters.query
        temp_l = []
        for clst in clusters:
            temp_l.append(self._get_geojson(clst))

        result['clusters'] = FeatureCollection(temp_l)
        return result


class Block(BaseEntity):
    # For all methods that start with Block

    def _get_geojson(self, block):
        # returns a geojson feature for the given DiseFFTTBasicData object.
        # FFTT = sesstion from/to. for 2010-11: 1011
        return Feature(
            geometry=Point(
                [block.centroid.x, block.centroid.y] if block.centroid is not None else []
            ),
            properties={
                'block_name': block.block_name,
                'district': block.district,
                'popupContent': ', '.join([block.block_name, block.district])
            },
            id=block.block_name
        )

    def _getschools(self, params):
        # returns list of schools in a given block
        # if format = geo, returns FeatureCollection
        # if format = plain, returns a plain list
        name = params.get('name')
        result = dict()
        result['query'] = params

        try:
            SchoolModel = get_models(params.get('session', '10-11'), 'school')

            temp_l = []
            school_api = School()
            schools = SchoolModel.objects.filter(
                block_name__iexact=name,
                # NOTE: Not sending schools without centroid
                # because there is no way to show them
                centroid__isnull=False
            )
            for sch in schools:
                temp_l.append(school_api._get_geojson(sch))
            result['schools'] = FeatureCollection(temp_l)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _search(self, params):
        # searches blocks and returns list
        result = dict()
        result['query'] = params
        BlockModel = get_models(params.get('session', '10-11'), 'block')

        if len(params.keys()) > 1:
            blocks = BlockModel.objects.filter(centroid__isnull=False)

        if 'name' in params and params.get('name', ''):
            blocks = blocks.filter(block_name__icontains=params.get('name'))

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73974609375,12.3906020692,79.447631375,13.4243520332"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                blocks = blocks.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            blocks = blocks[:params.get('limit')]

        # print blocks.query
        temp_l = []
        for blk in blocks:
            temp_l.append(self._get_geojson(blk))

        result['blocks'] = FeatureCollection(temp_l)
        return result


class District(BaseEntity):
    # For all methods that start with District
    def _getschools(self, params):
        # returns list of schools in a given district
        # if format = geo, returns FeatureCollection
        # if format = plain, returns a plain list
        name = params.get('name')
        result = dict()
        result['query'] = params

        try:
            SchoolModel = get_models(params.get('session', '10-11'), 'school')
            phormat = params.get('format')
            if phormat == 'geo':
                temp_l = []
                school_api = School()
                schools = SchoolModel.objects.filter(
                    district__iexact=name,
                    # NOTE: Not sending schools without centroid
                    # because there is no way to show them
                    centroid__isnull=False
                )
                for sch in schools:
                    temp_l.append(school_api._get_geojson(sch))
                result['schools'] = FeatureCollection(temp_l)
            else:
                schools = SchoolModel.objects.values(
                    'school_code', 'school_name'
                ).filter(district__iexact=name)
                result['schools'] = list(schools)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    @classmethod
    def getSchools(cls, params):
        # this just parses the dictionary from _getschools() and returns JSON
        result = cls()._getschools(params)
        if params.get('format', 'plain') == 'plain':
            return cls.to_json_str(result)
        elif params.get('format', 'plain') == 'geo':
            return cls.to_geojson_str(result)

    def _search(self, params):
        # searches districts and returns list
        result = dict()
        result['query'] = params
        DistrictModel = get_models(params.get('session', '10-11'), 'district')

        if len(params.keys()) > 1:
            districts = DistrictModel.objects.extra(
                select={
                    'centroid': 'ST_AsText(centroid)'
                }
            ).values(
                'district', 'centroid'
            )

        if 'name' in params and params.get('name', ''):
            districts = districts.filter(
                district__icontains=params.get('name')
            )

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73909375,12.52220692,79.447659375,13.424352095"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                districts = districts.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            districts = districts[:params.get('limit')]

        print districts.query
        result['districts'] = list(districts)
        return result


class Pincode(BaseEntity):
    # For all methods that start with Pincode
    def _getschools(self, params):
        # returns list of schools in a given pincode
        # if format = geo, returns FeatureCollection
        # if format = plain, returns a plain list
        pincode = params.get('pincode')
        result = dict()
        result['query'] = params

        try:
            SchoolModel = get_models(params.get('session', '10-11'), 'school')
            phormat = params.get('format')
            if phormat == 'geo':
                temp_l = []
                school_api = School()
                schools = SchoolModel.objects.filter(
                    pincode__iexact=pincode,
                    # NOTE: Not sending schools without centroid
                    # because there is no way to show them
                    centroid__isnull=False
                )
                for sch in schools:
                    temp_l.append(school_api._get_geojson(sch))
                result['schools'] = FeatureCollection(temp_l)
            else:
                schools = SchoolModel.objects.values(
                    'school_code', 'school_name'
                ).filter(pincode__iexact=pincode)
                result['schools'] = list(schools)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    @classmethod
    def getSchools(cls, params):
        # this just parses the dictionary from _getschools() and returns JSON
        result = cls()._getschools(params)
        if params.get('format', 'plain') == 'plain':
            return cls.to_json_str(result)
        elif params.get('format', 'plain') == 'geo':
            return cls.to_geojson_str(result)

    def _search(self, params):
        # searches pincodes and returns list
        result = dict()
        result['query'] = params
        PincodeModel = get_models(params.get('session', '10-11'), 'pincode')

        if len(params.keys()) > 1:
            pincodes = PincodeModel.objects.extra(
                select={
                    'centroid': 'ST_AsText(centroid)'
                }
            ).values(
                'pincode', 'centroid'
            )

        if 'pincode' in params and params.get('pincode', ''):
            pincodes = pincodes.filter(
                pincode__icontains=params.get('pincode')
            )

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73909375,12.52220692,79.447659375,13.424352095"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                pincodes = pincodes.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            pincodes = pincodes[:params.get('limit')]

        print pincodes.query
        result['pincodes'] = list(pincodes)
        return result
