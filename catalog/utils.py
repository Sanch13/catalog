import os


def get_upload_path_category_images(instance, filename):
    return os.path.join('files', instance.name, filename)


def get_file_upload_path_category(instance, filename):
    return os.path.join('files', instance.category.name, instance.name, filename)
