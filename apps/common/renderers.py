from rest_framework.renderers import JSONRenderer
from collections import OrderedDict


class DiseJSONRenderer(JSONRenderer):
    '''
        Sub-classes JSONRenderer to render GeoJSON where appropriate.
        If the request contains a geometry=yes parameter, it converts features
        to GeoJSON
    '''
    def render(self, data, media_type=None, renderer_context=None):
        # zfigure out whether we need to render geometry based on GET param

        rendered_data = {
            'results': {
                "type": "FeatureCollection",
                "features": data
            }
        }

        return super(DiseJSONRenderer, self).render(rendered_data, media_type,
                                                    renderer_context)
