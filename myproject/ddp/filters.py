import django_filters
from .models import Uploads, Shared
from django_filters import DateFilter
from django.contrib.auth.models import User as A_U

class UploadFilter(django_filters.FilterSet):

    start_date = DateFilter(field_name="u_date", lookup_expr='gte')
    end_date = DateFilter(field_name="u_date", lookup_expr='lte')
    class Meta:
        model = Uploads
        fields = '__all__'
        exclude = ['uploaded_by', 'u_hash' ]


class ShareFilter(django_filters.FilterSet):

    s_start_date = DateFilter(field_name="s_date", lookup_expr='gte')
    s_end_date = DateFilter(field_name="s_date", lookup_expr='lte')
    class Meta:
        model = Shared
        fields = '__all__'
        exclude = ['uploaded_by', 'u_hash' ]


class UsersFilter(django_filters.FilterSet):

    class Meta:
        model = A_U
        fields = '__all__'


class BlockedUsersFilter(django_filters.FilterSet):

    class Meta:
        model = A_U
        fields = '__all__'

