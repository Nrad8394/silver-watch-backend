from django.db.models import Q
from rest_framework.exceptions import PermissionDenied
from .models import CustomUser  # Import your custom user model

class RoleBasedQuerysetMixin:
    """
    Mixin to restrict queryset based on user roles, with optional `all=true` support for admins.
    """

    def get_filtered_queryset(self, model):
        user = self.request.user
        queryset = model.objects.all()

        # Superuser can access everything
        if user.is_superuser:
            return queryset

        all_requested = self.request.query_params.get("all") == "true"

        # Handle filtering for the CustomUser model itself
        if model == CustomUser:
            if user.role == "admin":
                return queryset if all_requested else queryset.filter(id=user.id)

            # Other roles can only see their own data
            return queryset.filter(id=user.id)

        # Get model fields dynamically
        model_fields = [field.name for field in model._meta.get_fields()]

        # Determine the correct user-related field
        user_field = None
        if "user" in model_fields:
            user_field = "user"
        elif "user_profile" in model_fields:
            user_field = "user_profile__user"

        # If no user-related field exists, deny access
        if not user_field:
            raise PermissionDenied(
                f"Access denied: Unauthorized model access. Available fields: {model_fields}"
            )

        # Role-based filtering
        role_filters = {
            "admin": Q(**{user_field: user.id}) if not all_requested else Q(),
            "caregiver": Q(**{user_field: user.id}),
            "technician": Q(**{user_field: user.id}),
            "patient": Q(**{user_field: user.id}),
        }

        return queryset.filter(role_filters.get(user.role, Q(**{user_field: user.id})))
