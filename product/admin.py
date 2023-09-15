from django.contrib import admin
from .models import Product, Categorie
from import_export.admin import ExportActionModelAdmin
from import_export import resources


    
class ProductResource(resources.ModelResource):

    class Meta:
        model = Product
        exclude = ('id', )

    def dehydrate_categorie(self, product):
        return product.categorie.name
    
class CategoryResource(resources.ModelResource):

    class Meta:
        model = Categorie
        exclude = ('id', )


class ProductAdmin(ExportActionModelAdmin):
    resource_classes = [ProductResource]
    list_display = ('id', 'name',
                    'price',
                    'store')
    list_display_links = ('id', 'name',)
    search_fields = ('name', 'store',)
    list_filter = ('categorie__name', 'store')
    list_per_page = 100

    def render_change_form(self, request, context, *args, **kwargs):
         context['adminform'].form.fields['categorie'].queryset = Categorie.objects.all()
         return super(ProductAdmin, self).render_change_form(request, context, *args, **kwargs)

class CateAdmin(ExportActionModelAdmin):
    resource_classes = [CategoryResource]
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 100




admin.site.register(Product, ProductAdmin)
admin.site.register(Categorie, CateAdmin)

