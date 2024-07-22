from django.utils.html import format_html
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .widgets import CustomClearableFileInput, CustomClearableFilesInput
from tinymce.widgets import TinyMCE

from catalog.models.catalog import Category
from catalog.models.file import CapFile
from catalog.models.cap import Cap


##############################################
# CAP MODEL
##############################################
class CapFileForm(forms.ModelForm):
    model = CapFile
    fields = ['file_type', 'file']
    widgets = {
        'file': CustomClearableFilesInput,
    }


class CapFileInline(admin.TabularInline):
    model = CapFile
    form = CapFileForm
    extra = 1

    def file_tag(self, obj):
        if obj.file:
            return format_html('<img src="{}" width="150" height="150" />', obj.file.url)
        return "No image"


class CapAdminForm(forms.ModelForm):
    class Meta:
        model = Cap
        fields = '__all__'
        widgets = {
            'description': TinyMCE(attrs={'cols': 80, 'rows': 30}),
            'name': forms.TextInput(attrs={'style': 'width: 500px;'}),
            'slug': forms.TextInput(attrs={'style': 'width: 500px;'}),
        }


@admin.register(Cap)
class CapAdmin(admin.ModelAdmin):
    form = CapAdminForm
    inlines = [CapFileInline]
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

    class Media:
        js = ('tinymce/tinymce.min.js', 'admin/js/tinymce_setup.js', 'admin/js/image-previews.js')
        css = {
            'all': ('admin/css/custom/styles.css',)
        }


##############################################
# CATEGORY MODEL
##############################################
class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'
        widgets = {
            'category_image': CustomClearableFileInput,
        }


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    form = CategoryAdminForm
    list_display = ('name', 'slug')
    prepopulated_fields = {"slug": ("name",)}

    def category_image_tag(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" width="150" height="150" />', obj.category_image.url)
        return "No Image"

    category_image_tag.short_description = 'Category Image'
    category_image_tag.allow_tags = True
