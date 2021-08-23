from django import forms
from .models import Post, Images

class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=128,label="Title",initial="Text")
    body = forms.CharField(max_length=245, label="Experience",initial="Text",widget=forms.Textarea)
 
    class Meta:
        model = Post
        fields = ('title', 'body', )
 
 
class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )

class CommentForm(forms.Form):
    comment = forms.CharField(required=True, max_length=500, min_length=3, strip=True)

