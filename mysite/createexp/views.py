
from django.shortcuts import render,get_object_or_404 ,redirect
from django.views import View
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .forms import ImageForm, PostForm ,CommentForm
from .models import Images,Post,Comment
from django.contrib.auth.decorators import login_required
from django.contrib.humanize.templatetags.humanize import naturaltime
from createexp.owner import OwnerDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import naturaltime
from createexp.utils import dump_queries
from django.db.models import Q


@login_required
def post(request,pk=None):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=3)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())
            
        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()
                
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(post=post_form, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request,"Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
                
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'createexp/add.html',{'postForm': postForm, 'formset': formset})


def ListView(request):
    model = Post
    strval = request.GET.get("search",False)
    if strval:
        query = Q(title__icontains=strval)
        query.add(Q(body__icontains=strval), Q.OR)
        objects = Post.objects.filter(query).select_related().order_by('-updated_at')[:10]
    else :
        objects = Post.objects.all().order_by('-updated_at')[:10]
        
    #objects = Post.objects.all().order_by('-updated_at')
    for obj in objects:
        obj.natural_updated = naturaltime(obj.updated_at)
    ctx = {'Exp_list' : objects, 'search': strval,}
    retval = render(request, 'createexp/Exp_list.html', ctx)

    dump_queries()
    return retval;

@login_required
def DetailView(request, id):
    post = get_object_or_404(Post, id=id)
    photos = Images.objects.filter(post=post)
    comments = Comment.objects.filter(post=post).order_by('-updated_at')
    comment_form = CommentForm()
    return render(request, 'createexp/Exp_detail.html', {
        'post':post,
        'photos':photos,
        'comments': comments, 
        'comment_form': comment_form
    })

def UpdateView(request,id):
    ImageFormSet = modelformset_factory(Images,form=ImageForm, extra=3)
    #'extra' means the number of photos that you can upload   ^
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id, user = request.user)
        postForm = PostForm(request.POST, request.FILES or None, instance=post)
        formset = ImageFormSet(request.POST, request.FILES,queryset=Images.objects.none())
        for imagecheck in formset.cleaned_data:
            if imagecheck:
                img = imagecheck['image']
                if img:
                    image_delete = Images.objects.filter(post=post).delete()
                else:
                    break
            else:
                break

        if postForm.is_valid() and formset.is_valid():
            post_form = postForm.save(commit=False)
            post_form.user = request.user
            post_form.save()

                
            for form in formset.cleaned_data:
                #this helps to not crash if the user   
                #do not upload all the photos
                if form:
                    image = form['image']
                    photo = Images(post=post_form, image=image)
                    photo.save()
            # use django messages framework
            messages.success(request,"Yeeew, check it out on the home page!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
                
    else:
        post = get_object_or_404(Post, id=id, user = request.user)
        postForm = PostForm(instance=post)
        formset = ImageFormSet(queryset=Images.objects.none())
    return render(request, 'createexp/add.html',{'postForm': postForm, 'formset': formset})


def DeleteView(request,id):
    ctx ={}
    if request.method == 'POST':
        post = get_object_or_404(Post, id=id, user = request.user)
        post.delete()
        return HttpResponseRedirect("/")
    
    return render (request,'createexp/Exp_delete.html',ctx)

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, request, id) :
        f = get_object_or_404(Post, id=id)
        comment = Comment(text=request.POST['comment'], user=request.user, post=f)
        comment.save()
        return redirect(reverse('createexp:Exp_detail', args=[id]))

class CommentDeleteView(OwnerDeleteView):
    model = Comment
    template_name = "createexp/comment_delete.html"

    # https://stackoverflow.com/questions/26290415/deleteview-with-a-dynamic-success-url-dependent-on-id
    def get_success_url(self):
        post = self.object.post
        return reverse('createexp:Exp_detail', args=[post.id])

