from rest_framework import mixins, viewsets


class ReadOnlyViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    A read-only viewset that allows only list and retrieve actions.
    """


class CreateUpdateViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    A mixin viewset that allows creating and updating objects.
    """


class DeviceBaseViewSet(viewsets.ModelViewSet):
    """
    A base viewset for device-related models with default permissions.
    """
    permission_classes = []  # Customize based on authentication needs
    filter_backends = []  # Add filtering, search, ordering backends if needed
