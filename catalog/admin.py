from django.utils.html import format_html
from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Series, Bottle, BottleFile, Jar, JarFile, Cap, CapFile
from .widgets import CustomClearableFileInput, CustomClearableFilesInput
from tinymce.widgets import TinyMCE


##############################################
# CAP MODEL
##############################################
class CapFileForm(forms.ModelForm):
    model = CapFile
    fields = ['file_type', 'file', 'rating']
    widgets = {
        'file': CustomClearableFilesInput,
    }


class CapFileInline(admin.TabularInline):
    model = CapFile
    form = CapFileForm
    extra = 5
    readonly_fields = ['thumbnail_display']

    def thumbnail_display(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="150" height="150" />')
        return "Нет изображения в Базе Данных"

    thumbnail_display.short_description = 'Миниатюра изображения'


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
# JAR MODEL
##############################################
class JarFileForm(forms.ModelForm):
    model = JarFile
    fields = ['file_type', 'file', 'rating']
    widgets = {
        'file': CustomClearableFilesInput,
    }


class JarFileInline(admin.TabularInline):
    model = JarFile
    form = JarFileForm
    extra = 5
    readonly_fields = ['thumbnail_display']

    def thumbnail_display(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="150" height="150" />')
        return "Нет изображения в Базе Данных"

    thumbnail_display.short_description = 'Миниатюра изображения'


@admin.register(Jar)
class JarAdmin(admin.ModelAdmin):
    form = JarFileForm
    inlines = [JarFileInline]
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('status', 'volume', )

    class Media:
        js = ('tinymce/tinymce.min.js', 'admin/js/tinymce_setup.js', 'admin/js/image-previews.js')
        css = {
            'all': ('admin/css/custom/styles.css',)
        }


##############################################
# BOTTLE MODEL
##############################################
class BottleFileForm(forms.ModelForm):
    model = BottleFile
    fields = ['file_type', 'file', 'rating']
    widgets = {
        'file': CustomClearableFilesInput,
    }


class BottleFileInline(admin.TabularInline):
    model = BottleFile
    form = BottleFileForm
    extra = 5
    readonly_fields = ['thumbnail_display']

    def thumbnail_display(self, obj):
        if obj.file:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="150" height="150" />')
        return "Нет изображения в Базе Данных"

    thumbnail_display.short_description = 'Миниатюра изображения'


@admin.register(Bottle)
class BottleAdmin(admin.ModelAdmin):
    form = BottleFileForm
    inlines = [BottleFileInline]
    list_display = ('name',)
    prepopulated_fields = {"slug": ("name",)}

    class Media:
        js = ('tinymce/tinymce.min.js', 'admin/js/tinymce_setup.js', 'admin/js/image-previews.js')
        css = {
            'all': ('admin/css/custom/styles.css',)
        }


##############################################
# SERIES MODEL
##############################################
class SeriesAdminForm(forms.ModelForm):
    class Meta:
        model = Series
        fields = '__all__'
        widgets = {
            'series_image': CustomClearableFileInput,
        }


@admin.register(Series)
class SeriesAdmin(admin.ModelAdmin):
    form = SeriesAdminForm
    list_display = ['id', 'name']
    list_display_links = ('id', 'name',)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('id',)

    class Media:
        css = {
            'all': ('admin/css/custom/styles.css',),
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
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name',)
    prepopulated_fields = {"slug": ("name",)}
    ordering = ('id',)

    class Media:
        css = {
            'all': ('admin/css/custom/styles.css',),
        }

    # def category_image_tag(self, obj):
    #     if obj.category_image:
    #         return format_html('<img src="{}"
    #         width="150"
    #         height="150" />',
    #         obj.category_image.url)
    #     return "No Image"

    # category_image_tag.short_description = 'Category Image'
    # category_image_tag.allow_tags = True
