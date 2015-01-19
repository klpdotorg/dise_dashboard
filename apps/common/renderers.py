# from rest_framework.renderers import JSONRenderer
# from shapely.wkt import loads as shapely_loads
# from shapely.geometry import mapping
# from collections import OrderedDict


# class DiseJSONRenderer(JSONRenderer):
#     '''
#         Sub-classes JSONRenderer to render GeoJSON where appropriate.
#         If the request contains a geometry=yes parameter, it converts features
#         to GeoJSON
#     '''

#     media_type = 'application/json'
#     format = 'json'

#     def render(self, data, media_type=None, renderer_context=None):
#         # zfigure out whether we need to render geometry based on GET param
#         render_geometry = renderer_context['request'].GET.get('geometry', 'no')
#         response_data = OrderedDict()

#         if render_geometry == 'yes':
#             # check if data has a 'count' property, which means a list
#             if 'count' in data.keys():
#                 # return featurecollection
#                 response_data['count'] = data['count']
#                 response_data['next'] = data['next']
#                 response_data['previous'] = data['previous']
#                 response_data['results'] = {
#                     "type": "FeatureCollection",
#                     "features": [
#                         dict(
#                             geometry=mapping(shapely_loads(entity.pop('centroid'))) if 'centroid' in entity else [],
#                             properties=entity,
#                             id=entity['school_code'],
#                             type="Feature"
#                         ) for entity in data['results']
#                     ]
#                 }
#             else:
#                 response_data['result'] = dict(
#                     geometry=mapping(shapely_loads(data.pop('centroid'))) if 'centroid' in data else [],
#                     properties=data,
#                     id=data['school_code'],
#                     type="Feature"
#                 )
#         else:
#             response_data = data

#         return super(DiseJSONRenderer, self).render(response_data, media_type,
#                                                     renderer_context)
