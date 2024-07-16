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
                f'<br><img src="{value.url}" width="100" height="100" id="image-preview" style="margin-top: 10px;"/>')
            return mark_safe(f'{input_html}{img_html}')
        return input_html

    class Media:
        js = ('admin/js/image-preview.js',)
