from django.urls import path, include

from data_schemas.views import HomeView, DataSchemaCreateView, DataSchemaUpdateView, DataSchemaListView, \
    DataSchemaDeleteView, DataSchemaDetailView, GenerateDataView, DownloadDataView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('schemas/', DataSchemaListView.as_view(), name='schemas_list'),
    path('schemas/create', DataSchemaCreateView.as_view(), name='new_schema'),
    path('schemas/<int:pk>/', DataSchemaDetailView.as_view(), name='schema_detail'),
    path('schemas/<int:pk>/edit', DataSchemaUpdateView.as_view(), name='schema_update'),
    path('schemas/<int:pk>/delete', DataSchemaDeleteView.as_view(), name='schema_delete'),
    path('schemas/<int:data_schema_id>/generate_data/', GenerateDataView.as_view(), name='generate_data'),
    path('schemas/<int:data_schema_id>/download', DownloadDataView.as_view(), name='download_csv'),
]

