from rest_framework import viewsets
from .serializers import SalarySerializer
from .models import Salary
from rest_framework.permissions import IsAdminUser


class SalaryViewSet(viewsets.ModelViewSet):
    """
    All methods are available for Admins.
    """
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
    permission_classes = [IsAdminUser]
