from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.core.paginator import Paginator
from django.http.request import HttpRequest

from django.http.response import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render

from utils.helpers import extract_hashtags, link_tags_to_post, object_id_generator

# from core.forms import FormWithCaptcha
from core.posts.forms import CreatePostForm
from core.posts.models import Post


@login_required
def create_post(request: HttpRequest) -> HttpResponse:
    # captcha = FormWithCaptcha()

    if request.method == "POST":
        post_form = CreatePostForm(request.POST, request.FILES)
        # TODO: remove this try/catch in production
        # try:
        #     captcha_data = request.POST["g-recaptcha-response"]
        # except:
        #     captcha_data = "..."

        # if not captcha_data == "" and not captcha_data == None:
        if post_form.is_valid():
            post_form = post_form.save(commit=False)
            post_form.user = request.user
                           
            object_id = object_id_generator(11, Post)
            post_form.object_id = object_id

            caption = request.POST["caption"]

            hashtags = extract_hashtags(text=caption)

            request.user.num_posts = request.user.num_posts + 1
            request.user.save()

            post_form.save()

            link_tags_to_post(post_id=object_id, tags=hashtags)

            return redirect("posts:get-post", post_id=object_id)

        else:
            messages.error(request, "Post creation failed")
        # else:
        #     messages.error(request, "Please confirm that you're not a robot")
    else:
        post_form = CreatePostForm()

    context = {
        "post_form": post_form,
    }
    return render(request, "private/submit_post.html", context)


def get_post(request: HttpRequest, post_id: str) -> HttpResponse:
    post = get_object_or_404(Post, object_id=post_id)
    context = {
        "post": post,
    }
    return render(request, "public/posts/view_post.html", context)


def frontpage(request: HttpRequest) -> HttpResponse:
    qs = Post.objects.all().order_by("-datetime_created")

    paginator = Paginator(qs, 20)

    try:
        page_number = int(request.GET.get("sida"))
    except:
        page_number = 1

    page_obj = paginator.get_page(page_number)

    context = {
        "posts": qs,
        # "page_obj": page_obj,
    }
    return render(request, "public/frontpage.html", context)


@login_required
def delete_post(request: HttpRequest, post_id: str) -> HttpResponseRedirect:
    try:
        post = Post.objects.get(object_id=post_id)
    except:
        raise Http404

    if not post.user == request.user:
        raise Http404

    else:
        post.delete()
        messages.success(request, "Your post has been deleted")
        return redirect("/")
