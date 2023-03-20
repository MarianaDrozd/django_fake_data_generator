import csv
import io
import os

from django.http import HttpResponse, Http404
from django.shortcuts import redirect
from django.views.generic import View, TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin

from faker import Faker

from fake_data_generator import settings
from .forms import DataColumnFormSet, DataSchemaForm
from .models import DataSchema, DataColumn, Dataset


class HomeView(LoginRequiredMixin, TemplateView):
    """A view for the homepage."""
    template_name = 'index.html'


class DataSchemaListView(LoginRequiredMixin, ListView):
    """A ListView for DataSchema model"""
    model = DataSchema
    context_object_name = 'schemas'
    template_name = 'data_schemas/list.html'

    def get_queryset(self):
        return DataSchema.objects.filter(user=self.request.user)


class DataSchemaCreateView(CreateView):
    """A CreateView for DataSchema model with inline formset usage for DataColumns. """
    form_class = DataSchemaForm
    model = DataSchema

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DataColumnFormSet(self.request.POST, prefix='schema_column', instance=self.object)
        else:
            data['formset'] = DataColumnFormSet(prefix='schema_column', instance=self.object)
        return data

    def form_valid(self, form):
        formset = DataColumnFormSet(self.request.POST, instance=self.object, prefix='schema_column')
        form.instance.user = self.request.user
        if formset.is_valid():
            self.object = form.save()
            for inline_form in formset.forms:
                if inline_form.has_changed():
                    inline_obj = inline_form.save(commit=False)
                    inline_obj.data_schema = self.object
                    inline_obj.save()
            for form in formset.extra_forms:  # Save dynamically added forms
                if form.has_changed():
                    inline_obj = form.save(commit=False)
                    inline_obj.data_schema = self.object
                    inline_obj.save()
            for inline_form in formset.deleted_forms:
                inline_form.instance.delete()  # Delete forms that were marked for deletion
            return redirect(self.get_success_url())
        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse("schemas_list")


class DataSchemaDetailView(LoginRequiredMixin, DetailView):
    """A DetailView for DataSchema model."""

    model = DataSchema
    context_object_name = 'schema'
    template_name = 'data_schemas/dataset_detail.html'

    def get_queryset(self):
        queryset = super(DataSchemaDetailView, self).get_queryset()
        pk = self.kwargs.get('pk', None)
        return DataSchema.objects.filter(id=pk)

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)

        return data


class DataSchemaUpdateView(LoginRequiredMixin, UpdateView):
    """An UpdateView for DataSchema model"""

    model = DataSchema
    fields = ["name"]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = DataColumnFormSet(self.request.POST, prefix='schema_column', instance=self.object)
        else:
            data['formset'] = DataColumnFormSet(prefix='schema_column', instance=self.object)
        return data

    def form_valid(self, form):
        formset = DataColumnFormSet(self.request.POST, instance=self.object, prefix='schema_column')
        form.instance.user = self.request.user
        if formset.is_valid():
            self.object = form.save()

            for inline_form in formset.forms:
                if inline_form.has_changed():
                    inline_obj = inline_form.save(commit=False)
                    inline_obj.data_schema = self.object
                    inline_obj.save()
            # Save dynamically added forms
            for form in formset.extra_forms:
                if form.has_changed():
                    inline_obj = form.save(commit=False)
                    inline_obj.data_schema = self.object
                    inline_obj.save()
            for inline_form in formset.deleted_forms:
                inline_form.instance.delete()  # Delete forms that were marked for deletion
            return redirect(self.get_success_url())

        return self.render_to_response(self.get_context_data(form=form, formset=formset))

    def get_success_url(self):
        return reverse("schemas_list")


class DataSchemaDeleteView(LoginRequiredMixin, DeleteView):
    """A DeleteView for DataSchema model"""

    model = DataSchema
    template_name = 'data_schemas/dataschema_confirm_delete.html'

    def get_success_url(self):
        return reverse("schemas_list")


class GenerateDataView(View):
    """A view for generating fake dataset"""

    def post(self, request, data_schema_id):
        # Get the data schema
        data_schema = DataSchema.objects.get(id=data_schema_id)
        sets = Dataset.objects.all()
        # Get the data columns for this schema
        data_columns = DataColumn.objects.filter(data_schema=data_schema).order_by('order')
        header = [column.name for column in data_columns]
        # Get the number of rows to generate
        num_of_records = request.POST['num_of_records']
        dataset = Dataset.objects.create(schema=data_schema, num_of_records=str(num_of_records))
        dataset.status = "processing"
        # Generate the data
        fake = Faker()
        data = []
        for i in range(int(num_of_records)):
            row = []
            for column in data_columns:
                if column.data_type == 'full_name':
                    row.append(fake.name())
                elif column.data_type == 'job':
                    row.append(fake.job())
                elif column.data_type == 'email':
                    row.append(fake.email())
                elif column.data_type == 'domain_name':
                    row.append(fake.domain_name())
                elif column.data_type == 'phone_number':
                    row.append(fake.phone_number())
                elif column.data_type == 'company_name':
                    row.append(fake.company())
                elif column.data_type == 'text':
                    row.append(fake.paragraph(nb_sentences=column.sentences_num, variable_nb_sentences=False))
                elif column.data_type == 'integer':
                    row.append(fake.random_int(min=column.start_num, max=column.end_num))
                elif column.data_type == 'address':
                    row.append(fake.address())
                elif column.data_type == 'date':
                    row.append(fake.date())
            data.append(row)

        # Write the data to a CSV file
        response = HttpResponse(content_type='text/csv')
        filename = f"{data_schema.name}_{num_of_records}.csv"
        # response['Content-Disposition'] = f'attachment; filename={filename}'

        directory = os.path.join(settings.MEDIA_ROOT)
        if not os.path.exists(directory):
            os.makedirs(directory)

        filepath = os.path.join(directory, filename)
        with io.open(filepath, mode='w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(header)
            for row in data:
                writer.writerow(row)

        # Create a dataset object and save it to the database
        dataset.csv_file = filepath
        dataset.status = 'ready'
        dataset.save()

        return redirect('schema_detail', data_schema_id)


class DownloadDataView(View):
    def get(self, request, data_schema_id):
        data = Dataset.objects.get(pk=data_schema_id)
        filepath = data.csv_file

        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                response = HttpResponse(f, content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{data.modified_at}.csv"'
                return response
        else:
            raise Http404("File not found")