from rest_framework import mixins, serializers, viewsets


class DeleteViewSet(mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    viewsets.GenericViewSet):
    pass


class GenreCatField(serializers.SlugRelatedField):
    def to_representation(self, value):
        ret = {
            'name': value.name,
            'slug': value.slug,
        }
        return ret
