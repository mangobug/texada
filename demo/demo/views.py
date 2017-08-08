# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import default_storage

from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import FormView
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from .models import Product
from .forms import ProductForm, UploadFileForm

import csv
import cStringIO as StringIO

from annoying.decorators import ajax_request
from datetime import timedelta, datetime


class HomePageView(TemplateView):
    """
    Home page view to view, record and track the location
    """
    template_name = 'demo/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['latest_products'] = Product.objects.all().order_by('product_id')
        return context


class ProductView(FormView):
    """
    Veiw a specific product and extract report
    """
    template_name = 'demo/product_view.html'
    form_class = ProductForm
    success_url = '/'


    def get_context_data(self, **kwargs):
        context = super(ProductView, self).get_context_data(**kwargs)
        try:
            product = Product.objects.get(id = self.kwargs['pk'])
        except ObjectDoesNotExist:
            product = None
        if product:
            context['products'] = Product.objects.filter(product_id = product.product_id)
        return context

    def form_valid(self, form):
        # This method is called when valid form data has been POSTed.
        # It should return an HttpResponse.
        #form.send_email()
        return super(ProductView, self).form_valid(form)

class ProductCreate(CreateView):
    """
    Create a new entry in the Product model
    """
    model = Product
    success_url="/"
    fields = ['product_id', 'description', 'datetime',
            'longitude', 'latitude', 'elevation']


class ProductUpdate(UpdateView):
    """
    Update a product entry
    """
    model = Product
    success_url="/"
    fields = ['product_id', 'description',
            'longitude', 'latitude', 'elevation']
    template_name_suffix = '_update_form'


class ExportView(View):
    """
    Export the data on the screen in a JSON format
    """
    def get(self, request, product_id = None):
        if product_id:
            leads_as_json = serializers.serialize('json', Product.objects.filter(product_id = product_id))
        else:
            leads_as_json = serializers.serialize('json', Product.objects.all())
        return HttpResponse(leads_as_json, content_type='text/plain')


class ExportAllView(View):
    """
    Export all the data in the database in TXT
    """
    def get(self, request):

        def data():
            """
            Traverse the content, place in file and return to client
            """
            products = Product.objects.all()
            csvfile = StringIO.StringIO()
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(["id", "description","datetime","longitude","latitude","elevation"])
            for product in products:
                csvwriter.writerow([str(product.product_id),
                        product.description,
                        str(product.datetime),
                        str(product.longitude),
                        str(product.latitude),
                        str(product.elevation)])
            yield csvfile.getvalue()

        response = HttpResponse(data(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename=test.csv"
        return response


def format_datetime(time):
    strs = time
    #replace the last ':' with an empty string, as python UTC offset format is +HHMM
    strs = strs[::-1].replace(':','',1)[::-1]
    try:
        offset = int(strs[-5:])
    except:
        print "Error"

    delta = timedelta(hours = offset / 100)

    time = datetime.strptime(strs[:-5], "%Y-%m-%dT%H:%M:%S")
    time -= delta                #reduce the delta from this time object

    return time

def import_data():

    with open('static_files/import.txt', 'rU') as f:
        for row in csv.reader(f.read().splitlines()[1:]):
            data = row[0].split('\t')
            time = format_datetime(data[2])
            obj, flag = Product.objects.get_or_create(
                                product_id = data[0],
                                description = data[1],
                                datetime = time,
                                longitude = data[3],
                                latitude = data[4],
                                elevation = data[5]
            )
    return True

def handle_uploaded_file(f):
    with open('static_files/import.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            import_data()
            return HttpResponseRedirect('/')
    else:
        form = UploadFileForm()
    return render(request, 'demo/import_data.html', {'form': form})

@ajax_request
def delete_product(request):
    p_id = request.GET.get('product_id')
    Product.objects.get(id = p_id).delete()
    return JsonResponse([True], safe=False)
