from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe


class CustomClearableFileInput(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    )
    template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs)
        if value and hasattr(value, "url"):
            img_html = mark_safe(
                f'<br>'
                f'<img src="{value.url}" '
                f'width="150" '
                f'height="150" '
                f'id="{value}"'
                f'style="margin-top: 10px;"/>')
            return mark_safe(f'{input_html}{img_html}')
        return input_html

    class Media:
        js = ('admin/js/image-preview.js',)


class CustomClearableFilesInput(ClearableFileInput):
    template_with_initial = (
        '%(initial_text)s: %(initial)s %(clear_template)s<br />%(input_text)s: %(input)s'
    )
    template_with_clear = '%(clear)s <label for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs)
        img_html = ''
        if value and hasattr(value, "url"):
            img_id = f"image-preview-{name.replace(':', '_')}"
            img_html = mark_safe(
                f'<br>'
                f'<img src="{value.url}" '
                f'width="150" '
                f'height="150" '
                f'id="{img_id}" '
                f'class="image-preview" '
                f'style="margin-top: 10px;"/>'
            )
        return mark_safe(f'{input_html}{img_html}')

    class Media:
        js = ('admin/js/image-previews.js',)
