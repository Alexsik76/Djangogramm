from django.forms import ModelForm
from gramm_app.models import Post


class PostCreateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.template_name = 'gramm_app/bulma_templates/widgets/clearable_file_input.html'

    class Meta:
        model = Post
        fields = ('title', 'image',)

    class Media:
        js = ('forms/file_field.js',)


class PostUpdateForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].widget.template_name = 'gramm_app/bulma_templates/widgets/clearable_file_input.html'

    class Meta:
        model = Post
        fields = ('title', 'image',)

    class Media:
        js = ('forms/file_field.js',)
