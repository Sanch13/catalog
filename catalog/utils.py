import os


def get_default_category():
    from catalog.models.category import Category
    return Category.objects.get(name=Category.Categories.BOTTLES)


def get_upload_path_category_or_series(instance, filename):
    return os.path.join('files', instance.name, filename)


def get_file_upload_path_category(instance, filename):
    return os.path.join('files', instance.category.name, instance.name, filename)
