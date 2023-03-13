from django.urls import path, include

from data_schemas.views import HomeView, DataSchemaCreateView, DataSchemaUpdateView, DataSchemaListView, \
    DataSchemaDeleteView, DataSchemaDetailView, GenerateDataView

urlpatterns = [
    path('', HomeView.as_view(), name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('new/', DataSchemaCreateView.as_view(), name='new_schema'),
    path('schemas/', DataSchemaListView.as_view(), name='schemas_list'),
    path('schemas/<int:pk>/', DataSchemaDetailView.as_view(), name='schema_detail'),
    path('schemas/<int:pk>/edit', DataSchemaUpdateView.as_view(), name='schema_update'),
    path('schemas/<int:pk>/delete', DataSchemaDeleteView.as_view(), name='schema_delete'),
    path('schemas/<int:data_schema_id>/generate_data/', GenerateDataView.as_view(), name='generate_data'),

    # path('schema/<int:pk>/generate_csv/', generate_dataset, name='generate_csv'),
    # path('schema/<int:pk>/download_csv/', generate_csv, name='download_csv'),
    # path('<int:schema_id>/generate-data/', generate_data_view, name='generate_data'),
    # path('<int:schema_id>/download-data/', download_data_view, name='download_data'),

]
