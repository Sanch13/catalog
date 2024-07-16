from django.contrib import admin
from django.utils.text import slugify
from django.utils.html import format_html

from .models import Product, File, Category


class FileInline(admin.TabularInline):
    model = File
    extra = 1

    def thumbnail(self, instance):
        return '<img src="{}" width="100" height="100" />'.format(instance.file.url)

    thumbnail.allow_tags = True
    thumbnail.short_description = 'Preview'

    fields = ('file', 'file_type', 'thumbnail',)
    readonly_fields = ('thumbnail',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'status')
    inlines = [FileInline]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'category_image')

    def category_image_tag(self, obj):
        if obj.category_image:
            return format_html('<img src="{}" width="100" height="100" />', obj.category_image.url)
        return "No Image"
    category_image_tag.short_description = 'Category Image'
    category_image_tag.allow_tags = True
