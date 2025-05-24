from django.contrib.auth.mixins import UserPassesTestMixin

from accounts.models import CustomUserType


class HasCustomerAccessPermission(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == CustomUserType.customer.value
        return False


class HasAdminAccessPermission(UserPassesTestMixin):

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.type == CustomUserType.admin.value
        return False
