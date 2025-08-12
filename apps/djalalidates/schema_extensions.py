from drf_spectacular.extensions import OpenApiSerializerFieldExtension

class JalaliDateFieldExtension(OpenApiSerializerFieldExtension):
    target_class = 'apps.djalalidates.serializers.JalaliDateField'  

    def map_serializer_field(self, auto_schema, direction):
        return {
            'type': 'string',
            'format': 'jalali-date',
            'example': '1404/05/21',
            'description': 'Date in Jalali (Shamsi) format yyyy/mm/dd'
        }