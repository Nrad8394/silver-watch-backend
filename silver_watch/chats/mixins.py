from rest_framework import permissions

class UserOwnedMixin:
    """
    Mixin to ensure users can only access their own related data.
    """

    def get_queryset(self):
        user = self.request.user
        queryset = super().get_queryset()

        if self.model_name == "conversation":
            return queryset.filter(participants=user)
        elif self.model_name == "message":
            return queryset.filter(conversation__participants=user)
        elif self.model_name == "contact":
            return queryset.filter(user=user)

        return queryset
