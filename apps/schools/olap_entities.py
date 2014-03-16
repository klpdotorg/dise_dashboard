import re
import urllib
import urllib2
import traceback
try: import simplejson as json
except ImportError: import json

from django.contrib.gis.geos import Polygon
from geojson import Feature, FeatureCollection, Point, dumps as geojson_dumps

from schools import olap_models
from schools.olap_models import get_models
from common.models import search_choices, YESNO, AREA, SCHOOL_CATEGORY, \
    SCHOOL_MANAGEMENT, SCHOOL_TYPES, MEDIUM, MDM_STATUS, KITCHENSHED_STATUS, BOUNDARY_WALL


class BaseEntity:
    # The private methods return Python objects
    # So that they can be used by other private methods
    # The classmethods return JSON that is sent as output

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
        obj = cls()
        result = obj._getschools(params)

        # Check if we should send back the entity
        include_entity = params.get('include_entity', False)
        if include_entity:
            print 'Entity object required, sending ..'
            entity_info = obj._getinfo(params)
            if obj.entity_type in entity_info:
                result[obj.entity_type] = entity_info[obj.entity_type]

        return cls.to_geojson_str(result)

    @classmethod
    def getBlocks(cls, params):
        # this just parses the dictionary from _getblocks() and returns JSON
        obj = cls()
        result = obj._getblocks(params)

        # Check if we should send back the entity
        include_entity = params.get('include_entity', False)
        if include_entity:
            entity_info = obj._getinfo(params)
            if obj.entity_type in entity_info:
                result[obj.entity_type] = entity_info[obj.entity_type]

        return cls.to_geojson_str(result)

    @classmethod
    def getClusters(cls, params):
        # this just parses the dictionary from _getclusters() and returns JSON
        obj = cls()
        result = obj._getclusters(params)

        # Check if we should send back the entity
        include_entity = params.get('include_entity', False)
        if include_entity:
            entity_info = obj._getinfo(params)
            if obj.entity_type in entity_info:
                result[obj.entity_type] = entity_info[obj.entity_type]

        return cls.to_geojson_str(result)

    def _get_geojson(self, entity):
        # returns a geojson feature for the given DiseFFTTBasicData object.
        # FFTT = sesstion from/to. for 2010-11: 1011
        if hasattr(self, 'display_field'):
            popup_content = [str(getattr(entity, self.display_field))]
        else:
            popup_content = [str(getattr(entity, self.primary_key))]

        if hasattr(self, 'secondary_key') and self.secondary_key:
            popup_content.append(str(getattr(entity, self.secondary_key)))

        properties = {
            'entity_type': self.entity_type,
            'popupContent': ', '.join(popup_content)
        }
        for field in self.only_fields:
            properties[field] = getattr(entity, field)
            if hasattr(entity, "get_{}_display".format(field)):
                properties[field + '_display'] = getattr(entity, "get_{}_display".format(field))()

        return Feature(
            geometry=Point(
                [entity.centroid.x,
                    entity.centroid.y] if entity.centroid is not None else []
            ),
            properties=properties,
            id=str(getattr(entity, self.primary_key))
        )

    def _getinfo(self, params):
        # gets the details of a school and returns a dictionary
        primary_key = params.get(self.param_name_for_primary_key)

        if type(primary_key) == str or type(primary_key) == unicode:
            primary_key = urllib.unquote_plus(primary_key)

        result = dict()
        result['query'] = params

        try:
            EntityModel = get_models(
                params.get('session', '10-11'), self.entity_type)
            filters = dict()
            filters[self.primary_key + '__iexact'] = primary_key

            if hasattr(self, 'secondary_key') and hasattr(self, 'param_name_for_secondary_key'):
                # required in case of a composite key like scenario
                # e.g. cluster_name is not unique. It needs block_name with it
                if self.secondary_key and self.param_name_for_secondary_key and params.get(self.param_name_for_secondary_key):
                    secondary_key = params.get(
                        self.param_name_for_secondary_key)
                    filters[self.secondary_key + '__iexact'] = secondary_key

            entity_obj = EntityModel.objects.get(**filters)

            result[self.entity_type] = self._get_geojson(entity_obj)
        except (EntityModel.DoesNotExist, Exception) as e:
            print 'filters', filters
            traceback.print_exc()
            result['error'] = str(e)
        return result


class School(BaseEntity):
    entity_type = 'school'
    display_field = 'school_name'

    primary_key = 'school_code'
    param_name_for_primary_key = 'code'
    secondary_key = ''
    param_name_for_secondary_key = ''

    only_fields = ['school_name', 'cluster_name',
                   'block_name', 'district', 'pincode', 'yeur_estd',
                   'total_boys', 'total_girls', 'male_tch', 'female_tch',
                   'medium_of_instruction', 'sch_management', 'sch_category',
                   'library_yn', 'books_in_library', 'no_of_computers',
                   'electricity', 'drinking_water', 'toilet_common', 'toilet_boys',
                   'toilet_girls', 'tot_clrooms']

    # For methods that start with `School`
    def _search(self, params):
        # This seaches all the base models, depending on the session and retuns
        # list of schools
        result = dict()
        result['query'] = params
        SchoolModel = get_models(params.get('session', '10-11'), 'school')

        if len(params.keys()) > 1:
            schools = SchoolModel.objects.only(*self.only_fields)

        if 'name' in params and params.get('name', ''):
            schools = schools.filter(school_name__icontains=params.get('name'))

        if 'cluster' in params and params.get('cluster', ''):
            schools = schools.filter(
                cluster_name__icontains=params.get('cluster'))

        if 'block' in params and params.get('block', ''):
            schools = schools.filter(
                block_name__icontains=params.get('block'))

        if 'district' in params and params.get('district', ''):
            schools = schools.filter(
                district__icontains=params.get('district'))

        if 'limit' in params and params.get('limit', 0):
            schools = schools[:params.get('limit')]

        if 'area' in params and params.get('area', ''):
            schools = schools.filter(
                rural_urban=search_choices(AREA, params.get('area').title())
            )

        if 'management' in params and params.get('management', ''):
            if params.get('management') == 'govt':
                schools = schools.filter(
                    sch_management__in=[1, 7]
                )
            elif params.get('management') == 'pvt':
                schools = schools.exclude(
                    sch_management__in=[1, 7]
                )

        if 'f' in params and params.get('f', ''):
            f = params.get('f')
            f = json.loads(urllib2.unquote(f).decode('utf8'))

            for filt in f.get('facilities', []):
                if filt == 'repair':
                    schools = schools.filter(
                        classrooms_require_minor_repair=search_choices(YESNO, 'Yes'),
                        classrooms_require_major_repair=search_choices(YESNO, 'Yes')
                    )
                elif filt == 'toilet':
                    schools = schools.filter(
                        toilet_common=0,
                        toilet_boys=0,
                        toilet_girls=0
                    )
                elif filt == 'toilet_for_girls':
                    schools = schools.filter(
                        toilet_girls=0
                    )
                elif filt == 'electricity':
                    schools = schools.filter(
                        electricity=search_choices(YESNO, 'No')
                    )
                elif filt == 'secure_wall':
                    schools = schools.exclude(
                        boundary_wall__in=[
                            search_choices(BOUNDARY_WALL, "Pucca"),
                            search_choices(BOUNDARY_WALL, "Barbed wire fencing"),
                        ]
                    )
                elif filt == 'library':
                    schools = schools.filter(
                        library_yn=search_choices(YESNO, 'No')
                    )
                elif filt == 'ramp':
                    schools = schools.filter(
                        ramps=search_choices(YESNO, 'No')
                    )
                elif filt == 'blackboard':
                    schools = schools.filter(
                        blackboard=search_choices(YESNO, 'No')
                    )
                elif filt == 'playground':
                    schools = schools.filter(
                        playground=search_choices(YESNO, 'No')
                    )
                elif filt == 'drinking_water':
                    schools = schools.filter(
                        drinking_water=search_choices(YESNO, 'No')
                    )

        result['total_count'] = schools.count()

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73974609375,12.5223906020692,79.4476318359375,13.424352095715332"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(
                r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                schools = schools.filter(centroid__contained=geom)

        print schools.query
        temp_l = []
        for sch in schools:
            temp_l.append(self._get_geojson(sch))
        result['results'] = FeatureCollection(temp_l)
        return result


class Cluster(BaseEntity):
    entity_type = 'cluster'

    primary_key = 'cluster_name'
    param_name_for_primary_key = 'name'
    secondary_key = 'block_name'
    param_name_for_secondary_key = 'block'

    only_fields = [
        'cluster_name', 'block_name', 'district', 'sum_boys', 'sum_girls', 'sum_schools', 'sum_male_tch',
        'sum_female_tch', 'sum_has_library', 'sum_has_electricity', 'sum_toilet_common', 'sum_toilet_boys',
        'sum_toilet_girls', 'sum_tot_clrooms', 'sum_classrooms_in_good_condition', 'sum_classrooms_require_minor_repair',
        'sum_classrooms_require_major_repair']

    # For all methods that start with Cluster
    def _getschools(self, params):
        # returns list of schools in a given cluster
        name = urllib.unquote_plus(params.get('name'))
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
            result['results'] = FeatureCollection(temp_l)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _search(self, params):
        # searches clusters and returns list
        result = dict()
        result['query'] = params
        ClusterModel = get_models(params.get('session', '10-11'), 'cluster')

        clusters = ClusterModel.objects.filter(centroid__isnull=False)

        if 'name' in params and params.get('name', ''):
            clusters = clusters.filter(
                cluster_name__icontains=params.get('name'))

        if 'block' in params and params.get('block', ''):
            clusters = clusters.filter(
                block_name__icontains=params.get('block'))

        result['total_count'] = clusters.count()

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73974609375,12.5223906020692,79.4476318359375,13.424352095715332"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(
                r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
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

        result['results'] = FeatureCollection(temp_l)
        return result


class Block(BaseEntity):
    # For all methods that start with Block
    entity_type = 'block'

    primary_key = 'block_name'
    param_name_for_primary_key = 'name'
    secondary_key = ''
    param_name_for_secondary_key = ''

    only_fields = [
        'block_name', 'district', 'sum_boys', 'sum_girls', 'sum_schools', 'sum_male_tch',
        'sum_female_tch', 'sum_has_library', 'sum_has_electricity', 'sum_toilet_common',
        'sum_toilet_boys', 'sum_toilet_girls', 'sum_tot_clrooms', 'sum_classrooms_in_good_condition',
        'sum_classrooms_require_minor_repair', 'sum_classrooms_require_major_repair']

    def _getschools(self, params):
        # returns list of schools in a given block
        name = urllib.unquote_plus(params.get('name'))
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
            result['results'] = FeatureCollection(temp_l)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _getclusters(self, params):
        # returns list of clusters in a given district
        name = urllib.unquote_plus(params.get('name'))
        result = dict()
        result['query'] = params

        try:
            ClusterModel = get_models(params.get('session', '10-11'), 'cluster')

            temp_l = []
            cluster_api = Cluster()
            clusters = ClusterModel.objects.filter(
                block_name__iexact=name,
                # NOTE: Not sending clusters without centroid
                # because there is no way to show them
                centroid__isnull=False
            )
            for sch in clusters:
                temp_l.append(cluster_api._get_geojson(sch))
            result['results'] = FeatureCollection(temp_l)

        except (ClusterModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _search(self, params):
        # searches blocks and returns list
        result = dict()
        result['query'] = params
        BlockModel = get_models(params.get('session', '10-11'), 'block')

        if len(params.keys()) > 1:
            blocks = BlockModel.objects.only(*self.only_fields).filter(centroid__isnull=False)

        if 'name' in params and params.get('name', ''):
            blocks = blocks.filter(block_name__icontains=params.get('name'))

        result['total_count'] = blocks.count()

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73974609375,12.3906020692,79.447631375,13.4243520332"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(
                r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
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

        result['results'] = FeatureCollection(temp_l)
        return result


class District(BaseEntity):
    # For all methods that start with District
    entity_type = 'district'

    primary_key = 'district'
    param_name_for_primary_key = 'name'
    secondary_key = ''
    param_name_for_secondary_key = ''

    only_fields = [
        'district', 'sum_boys', 'sum_girls', 'sum_schools', 'sum_male_tch',
        'sum_female_tch', 'sum_has_library', 'sum_has_electricity', 'sum_toilet_common',
        'sum_toilet_boys', 'sum_toilet_girls', 'sum_tot_clrooms', 'sum_classrooms_in_good_condition',
        'sum_classrooms_require_minor_repair', 'sum_classrooms_require_major_repair']

    def _getschools(self, params):
        # returns list of schools in a given district
        name = urllib.unquote_plus(params.get('name'))
        result = dict()
        result['query'] = params

        try:
            SchoolModel = get_models(params.get('session', '10-11'), 'school')

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
            result['results'] = FeatureCollection(temp_l)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _getclusters(self, params):
        # returns list of clusters in a given district
        name = urllib.unquote_plus(params.get('name'))
        result = dict()
        result['query'] = params

        try:
            ClusterModel = get_models(params.get('session', '10-11'), 'cluster')

            temp_l = []
            cluster_api = Cluster()
            clusters = ClusterModel.objects.filter(
                district__iexact=name,
                # NOTE: Not sending clusters without centroid
                # because there is no way to show them
                centroid__isnull=False
            )
            for sch in clusters:
                temp_l.append(cluster_api._get_geojson(sch))
            result['results'] = FeatureCollection(temp_l)

        except (ClusterModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _getblocks(self, params):
        # returns list of blocks in a given district
        name = urllib.unquote_plus(params.get('name'))
        result = dict()
        result['query'] = params

        try:
            BlockModel = get_models(params.get('session', '10-11'), 'block')

            temp_l = []
            block_api = Block()
            blocks = BlockModel.objects.filter(
                district__iexact=name,
                # NOTE: Not sending blocks without centroid
                # because there is no way to show them
                centroid__isnull=False
            )
            for sch in blocks:
                temp_l.append(block_api._get_geojson(sch))
            result['results'] = FeatureCollection(temp_l)

        except (BlockModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _search(self, params):
        # searches districts and returns list
        result = dict()
        result['query'] = params
        DistrictModel = get_models(params.get('session', '10-11'), 'district')

        if len(params.keys()) > 1:
            districts = DistrictModel.objects.only(*self.only_fields).filter(centroid__isnull=False)

        if 'name' in params and params.get('name', ''):
            districts = districts.filter(
                district__icontains=params.get('name')
            )

        result['total_count'] = districts.count()

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73909375,12.52220692,79.447659375,13.424352095"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(
                r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                districts = districts.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            districts = districts[:params.get('limit')]

        print districts.query
        temp_l = []
        for dist in districts:
            temp_l.append(self._get_geojson(dist))

        result['results'] = FeatureCollection(temp_l)
        return result


class Pincode(BaseEntity):
    # For all methods that start with Pincode
    entity_type = 'pincode'

    primary_key = 'pincode'
    param_name_for_primary_key = 'pincode'
    secondary_key = ''
    param_name_for_secondary_key = ''

    only_fields = [
        'pincode', 'sum_boys', 'sum_girls', 'sum_schools', 'sum_male_tch',
        'sum_female_tch', 'sum_has_library', 'sum_has_electricity', 'sum_toilet_common',
        'sum_toilet_boys', 'sum_toilet_girls', 'sum_tot_clrooms', 'sum_classrooms_in_good_condition',
        'sum_classrooms_require_minor_repair', 'sum_classrooms_require_major_repair']

    def _getschools(self, params):
        # returns list of schools in a given pincode
        pincode = params.get('pincode')
        result = dict()
        result['query'] = params

        try:
            SchoolModel = get_models(params.get('session', '10-11'), 'school')

            temp_l = []
            school_api = School()
            schools = SchoolModel.objects.filter(
                pincode__iexact=pincode,
                # NOTE: Not sending schools without centroid
                # because there is no way to show them
                centroid__isnull=False
            )

            result['total_count'] = schools.count()

            for sch in schools:
                temp_l.append(school_api._get_geojson(sch))
            result['results'] = FeatureCollection(temp_l)

        except (SchoolModel.DoesNotExist, Exception) as e:
            result['error'] = str(e)
        return result

    def _search(self, params):
        # searches pincodes and returns list
        result = dict()
        result['query'] = params
        PincodeModel = get_models(params.get('session', '10-11'), 'pincode')

        if len(params.keys()) > 1:
            pincodes = PincodeModel.objects.filter(centroid__isnull=False)

        if 'pincode' in params and params.get('pincode', ''):
            pincodes = pincodes.filter(
                pincode__icontains=params.get('pincode')
            )

        result['total_count'] = pincodes.count()

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73909375,12.52220692,79.447659375,13.424352095"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(
                r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                pincodes = pincodes.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            pincodes = pincodes[:params.get('limit')]

        # print pincodes.query
        temp_l = []
        for pin in pincodes:
            temp_l.append(self._get_geojson(pin))
        result['results'] = FeatureCollection(temp_l)
        return result


class Assembly(BaseEntity):
    # For all methods that start with Pincode
    entity_type = 'assembly'

    primary_key = 'assembly_name'
    param_name_for_primary_key = 'name'
    secondary_key = ''
    param_name_for_secondary_key = ''

    only_fields = [
        'assembly_name', 'sum_boys', 'sum_girls', 'sum_schools', 'sum_male_tch',
        'sum_female_tch', 'sum_has_library', 'sum_has_electricity', 'sum_toilet_common',
        'sum_toilet_boys', 'sum_toilet_girls', 'sum_tot_clrooms', 'sum_classrooms_in_good_condition',
        'sum_classrooms_require_minor_repair', 'sum_classrooms_require_major_repair']

    def _getschools(self, params):
        # returns list of schools in a given assembly_name
        assembly_name = urllib.unquote_plus(params.get(self.param_name_for_primary_key))

        result = dict()
        result['query'] = params

        SchoolModel = get_models(params.get('session', '10-11'), 'school')

        temp_l = []
        school_api = School()
        schools = SchoolModel.objects.filter(
            assembly_name__iexact=assembly_name,
            # NOTE: Not sending schools without centroid
            # because there is no way to show them
            centroid__isnull=False
        )

        result['total_count'] = schools.count()

        for sch in schools:
            temp_l.append(school_api._get_geojson(sch))
        result['results'] = FeatureCollection(temp_l)

        return result

    def _search(self, params):
        # searches pincodes and returns list
        result = dict()
        result['query'] = params
        AssemblyModel = get_models(params.get('session', '10-11'), 'assembly')

        if len(params.keys()) > 1:
            assemblies = AssemblyModel.objects.filter(centroid__isnull=False)

        if 'assembly' in params and params.get('assembly', ''):
            assemblies = assemblies.filter(
                assembly_name__icontains=params.get('assembly')
            )

        result['total_count'] = assemblies.count()

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73909375,12.52220692,79.447659375,13.424352095"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(
                r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                assemblies = assemblies.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            assemblies = assemblies[:params.get('limit')]

        # print assemblies.query
        temp_l = []
        for mla in assemblies:
            temp_l.append(self._get_geojson(mla))
        result['results'] = FeatureCollection(temp_l)
        return result


class Parliament(BaseEntity):
    # For all methods that start with Pincode
    entity_type = 'parliament'

    primary_key = 'parliament_name'
    param_name_for_primary_key = 'name'
    secondary_key = ''
    param_name_for_secondary_key = ''

    only_fields = [
        'parliament_name', 'sum_boys', 'sum_girls', 'sum_schools', 'sum_male_tch',
        'sum_female_tch', 'sum_has_library', 'sum_has_electricity', 'sum_toilet_common',
        'sum_toilet_boys', 'sum_toilet_girls', 'sum_tot_clrooms', 'sum_classrooms_in_good_condition',
        'sum_classrooms_require_minor_repair', 'sum_classrooms_require_major_repair']

    def _getschools(self, params):
        # returns list of schools in a given parliament
        parliament_name = urllib.unquote_plus(params.get(self.param_name_for_primary_key))

        result = dict()
        result['query'] = params

        SchoolModel = get_models(params.get('session', '10-11'), 'school')

        temp_l = []
        school_api = School()
        schools = SchoolModel.objects.filter(
            parliament_name__iexact=parliament_name,
            # NOTE: Not sending schools without centroid
            # because there is no way to show them
            centroid__isnull=False
        )

        result['total_count'] = schools.count()

        for sch in schools:
            temp_l.append(school_api._get_geojson(sch))
        result['results'] = FeatureCollection(temp_l)

        return result

    def _search(self, params):
        # searches pincodes and returns list
        result = dict()
        result['query'] = params
        ParliamentModel = get_models(params.get('session', '10-11'), 'parliament')

        if len(params.keys()) > 1:
            parliaments = ParliamentModel.objects.filter(centroid__isnull=False)

        if 'parliament' in params and params.get('parliament', ''):
            parliaments = parliaments.filter(
                parliament_name__icontains=params.get('parliament')
            )

        result['total_count'] = parliaments.count()

        if 'bbox' in params and params.get('bbox', ''):
            # &bbox="75.73909375,12.52220692,79.447659375,13.424352095"
            # southwest_lng,southwest_lat,northeast_lng,northeast_lat
            # xmin,ymin,xmax,ymax
            coords_match = re.match(
                r"([\d\.]+),([\d\.]+),([\d\.]+),([\d\.]+)", params.get('bbox'))
            if coords_match and len(coords_match.groups()) == 4:
                bbox = map(lambda x: float(x), coords_match.groups())
                geom = Polygon.from_bbox(bbox)
                parliaments = parliaments.filter(centroid__contained=geom)

        if 'limit' in params and params.get('limit', 0):
            parliaments = parliaments[:params.get('limit')]

        # print parliaments.query
        temp_l = []
        for mp in parliaments:
            temp_l.append(self._get_geojson(mp))
        result['results'] = FeatureCollection(temp_l)
        return result
