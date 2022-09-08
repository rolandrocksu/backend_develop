"""
Explanation
With the PermissionPolicyMixin mixin we alter the permission process of Django Rest Framework.
Before checking the permission for an endpoint we check if the method associated exists in
the permission_classes_per_method attribute. If so, we set self.permission_classes.

This mixin also allows us to override the permission_classes set in the @action() decorator. So it can also help
to define all the permission policies in one place.

Note: When a ViewSet inherits of PermissionPolicyMixin, it is important that the mixin is set first, or
at least before any classes like *ViewSet or *ModelMixin.
"""

class PermissionPolicyMixin:
    def check_permissions(self, request):
        try:
            # This line is heavily inspired from `APIView.dispatch`.
            # It returns the method associated with an endpoint.
            handler = getattr(self, request.method.lower())
        except AttributeError:
            handler = None

        if (
            handler
            and self.permission_classes_per_method
            and self.permission_classes_per_method.get(handler.__name__)
        ):
            self.permission_classes = self.permission_classes_per_method.get(handler.__name__)

        super().check_permissions(request)


