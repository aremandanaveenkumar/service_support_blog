from .models import Comment, Post, AddressField
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'featured_image', 
                  'customer', 'customer_address', 'problem_reported', 
                  'rectification', 'status', 'excerpt']
        exclude = ['slug', ]
        widgets = {'problem_reported': SummernoteWidget(),  
                   'rectification': SummernoteWidget()}


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressField
        fields = ['street', 'city', 'state', 'postal_code', 'country']

    def clean(self):
        cleaned_data = super().clean()
        if AddressField.objects.filter(
            street=cleaned_data.get("street"),
            city=cleaned_data.get("city"),
            state=cleaned_data.get("state"),
            postal_code=cleaned_data.get("postal_code"),
            country=cleaned_data.get("country")
        ).exists():
            raise forms.ValidationError("This address already exists!")
        return cleaned_data
