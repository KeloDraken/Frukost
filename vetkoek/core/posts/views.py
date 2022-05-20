from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http.request import HttpRequest
from django.http.response import Http404
from django.shortcuts import get_object_or_404, redirect, render

# from core.forms import FormWithCaptcha
from vetkoek.core.posts.forms import CreatePostForm
from vetkoek.core.posts.models import Post
from vetkoek.utils.helpers import (
    extract_hashtags,
    link_tags_to_post,
    object_id_generator,
)


@login_required
def create_post(request: HttpRequest):
    """
    The function takes in a request object, checks if the request is a POST request, and if it is, it creates a new post
    object and saves it to the database

    :param request: The request object
    :type request: HttpRequest
    :return: A post object
    """

    if not request.method == "POST":
        post_form = CreatePostForm()
    else:
        post_form = CreatePostForm(request.POST, request.FILES)
        # TODO: remove this try/catch in production
        # captcha = FormWithCaptcha()
        # try:
        #     captcha_data = request.POST["g-recaptcha-response"]
        # except:
        #     captcha_data = "..."

        # if captcha_data == "" or captcha_data is None:
        #     messages.error(request, "Please confirm that you're not a robot")

        if post_form.is_valid():
            messages.error(request, "Post creation failed")
        else:
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
    context = {
        "post_form": post_form,
    }
    return render(request, "private/submit_post.html", context)


def get_post(request: HttpRequest, post_id: str):
    """
    "Get the post with the given ID, or return a 404 error if it doesn't exist."

    The first line of the function is a type hint. It tells the Python interpreter that the first argument to the function
    is an HttpRequest object, and the second argument is a string

    :param request: The request object that was sent to the view
    :type request: HttpRequest
    :param post_id: The ID of the post we want to view
    :type post_id: str
    :return: A post object
    """
    post = get_object_or_404(Post, object_id=post_id)
    context = {
        "post": post,
    }
    return render(request, "public/posts/view_post.html", context)


def frontpage(request: HttpRequest):
    """
    "Get the page number from the request, get the posts from the database, paginate them, and render the template."

    The first thing we do is try to get the page number from the request. If the page number is not a valid integer, we
    default to page 1

    :param request: The request object
    :type request: HttpRequest
    :return: A HttpResponse object with the rendered template.
    """
    try:
        page_number = int(request.GET.get("sida"))
    except ValueError:
        page_number = 1
    except TypeError:
        page_number = 1


    qs = Post.objects.all().order_by("-datetime_created")
    paginator = Paginator(qs, 15)
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
    }
    return render(request, "public/frontpage.html", context)


@login_required
def delete_post(request: HttpRequest, post_id: str):
    """
    If the post exists, and the user is the owner of the post, delete the post and redirect to the homepage

    :param request: HttpRequest
    :type request: HttpRequest
    :param post_id: The id of the post we want to delete
    :type post_id: str
    :return: the redirect function.
    """
    try:
        post = Post.objects.get(object_id=post_id)
    except Post.DoesNotExist:
        raise Http404

    if not post.user == request.user:
        raise Http404

    else:
        post.delete()
        messages.success(request, "Your post has been deleted")
        return redirect("/")
