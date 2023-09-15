from django.shortcuts import render
from django import forms
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Product, Categorie
from .serializers import AddProductSerializer
import requests
import json
from io import BytesIO
from django.core.files import File
from urllib.parse import urlparse
from product.scripts.amazon import scrape_amazon
from product.scripts.sephora import scrap_sephora
from product.scripts.shein import scrap_shein
from product.scripts.aliexpress import scrap_aliexpress
import traceback
from product.models import Categorie

att = {
    'class': 'form-control',
    'style': 'width: 100%;padding: 10px;border: 1px solid #ccc;border-radius: 4px;box-sizing: border-box;font-size: 16px;margin-top: 10px;margin-bottom: 10px;',
        
}


class FileUploadForm(forms.Form):
    categories = forms.ModelChoiceField(queryset=Categorie.objects.all(), required=True,widget=forms.Select(attrs={'class': 'form-control',
                                                'style': 'width: 100%;height: 45px ;border: 1px solid #ccc;border-radius: 4px;box-sizing: border-box;font-size: 16px;margin-top: 10px;margin-bottom: 10px;',}))
    
    store = forms.ChoiceField(label='Store',required=True,
                                       choices=[('amazon', 'Amazon'), ('aliexpress', 'AliExpress (EUR)'),
                                                ('sephora', 'Sephora (USD)'),
                                                ('shein', 'Shein')], widget=forms.Select(attrs={'class': 'form-control',
                                                'style': 'width: 100%;height: 45px ;border: 1px solid #ccc;border-radius: 4px;box-sizing: border-box;font-size: 16px;margin-top: 10px;margin-bottom: 10px;',}))
    urls = forms.CharField(label='URLs (seperated by newline)', widget=forms.Textarea, required=True )
    percentage = forms.FloatField(widget=forms.NumberInput(attrs=att),required=True)
    max_value = forms.FloatField(label="Max price value (DZD)",widget=forms.NumberInput(attrs=att), required=True)
    more = forms.FloatField(label="Extra cost if more (DZD)",widget=forms.NumberInput(attrs=att), required=True)
    less = forms.FloatField(label="Extra cost if less (DZD)",widget=forms.NumberInput(attrs=att), required=True)


@login_required(login_url='/admin/login')
def upload_view(request):
    """
    Add products, only for admin, retrieve the form, the scrap the urls
    """
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            urls = form.cleaned_data['urls']
            category = form.cleaned_data['categories']
            original_store = form.cleaned_data['store']
            percentage = form.cleaned_data['percentage']
            maxVal = form.cleaned_data['max_value']
            more = form.cleaned_data['more']
            less = form.cleaned_data['less']
            output = process_data(urls, category, original_store, percentage, maxVal, more, less)
            return render(request, 'product/add_product.html', {'form': form, 'output': output})
    else:
        form = FileUploadForm()
    return render(request, 'product/add_product.html', {'form': form})


def process_data(urls, categorie, store, perc, maxVal ,more, less):
    """
    We scape entire page, then send data to serializer, if everything is ok, add it to db
    """
    try:
        ret = {}
        categorie = Categorie.objects.get(name=categorie).pk
        for url in urls.split("\r\n"):
                if store=="amazon":
                    scrape_amazon(url, perc, "amazon", categorie, maxVal, more, less)
                elif store == "shein":                    
                    scrap_shein(url, perc, "shein", categorie,maxVal, more, less)
                elif store == "sephora":
                    scrap_sephora(url, perc, "sephora", categorie, maxVal, more, less)
                elif store == "aliexpress":
                    scrap_aliexpress(url, perc, "aliexpress", categorie, maxVal, more, less)
                else:
                    break
        ret["details"] = "Upload is over"
        return ret
    except Exception as e: 
        traceback.print_exc()
        # if there was an issue
        return {"details": "Upload is over, if you cant find the new products, either url is incorrect or url blocked by host","error":e}
