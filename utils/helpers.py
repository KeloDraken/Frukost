import random
import string
from typing import List

from django.core.exceptions import ObjectDoesNotExist

from core.posts.models import Post, PostTag, Tag


def forbidden_attributes():
    """
    It returns a list of all the attributes that are forbidden in HTML
    :return: A list of forbidden attributes.
    """
    return [
        "iframe",
        "<iframe>",
        "</iframe>",
        "script",
        "<script>",
        "</script>",
        "<link>",
        "</link>",
        "onabort",
        "onanimationcancel",
        "onanimationend",
        "onanimationiteration",
        "onanimationstart",
        "onauxclick",
        "onbeforeinput",
        "onblur",
        "oncanplay",
        "oncanplaythrough",
        "onchange",
        "onclick",
        "onclose",
        "oncontextmenu",
        "oncopy",
        "oncuechange",
        "oncut",
        "ondblclick",
        "ondrag",
        "ondragend",
        "ondragenter",
        "ondragexit",
        "ondragleave",
        "ondragover",
        "ondragstart",
        "ondrop",
        "ondurationchange",
        "onemptied",
        "onended",
        "onerror",
        "onfocus",
        "onformdata",
        "onfullscreenchange",
        "onfullscreenerror",
        "ongotpointercapture",
        "oninput",
        "oninvalid",
        "onkeydown",
        "onkeypress",
        "onkeyup",
        "onload",
        "onloadeddata",
        "onloadedmetadata",
        "onloadend",
        "onloadstart",
        "onlostpointercapture",
        "onmousedown",
        "onmouseenter",
        "onmouseleave",
        "onmousemove",
        "onmouseout",
        "onmouseover",
        "onmouseup",
        "onmozfullscreenchange",
        "onmozfullscreenerror",
        "onpaste",
        "onpause",
        "onplay",
        "onplaying",
        "onpointercancel",
        "onpointerdown",
        "onpointerenter",
        "onpointerleave",
        "onpointermove",
        "onpointerout",
        "onpointerover",
        "onpointerup",
        "onprogress",
        "onratechange",
        "onreset",
        "onresize",
        "onscroll",
        "onseeked",
        "onseeking",
        "onselect",
        "onselectstart",
        "onstalled",
        "onsubmit",
        "onsuspend",
        "ontimeupdate",
        "ontoggle",
        "ontransitioncancel",
        "ontransitionend",
        "ontransitionrun",
        "ontransitionstart",
        "onvolumechange",
        "onwaiting",
        "onwebkitanimationend",
        "onwebkitanimationiteration",
        "onwebkitanimationstart",
        "onwebkittransitionend",
        "onwheel",
    ]


def extract_hashtags(text: str):
    """
    function to extract all the hashtags in a product description.
    It generates new `Tag` instance, if it does not exist, for each of
    of the tags
    """
    hashtag_list: List[str] = list()

    for word in text.split():
        if word[0] == "#":
            hashtag_list.append(word[1:])

    for hashtag in hashtag_list:
        obj, created = Tag.objects.get_or_create(
            name=hashtag.lower(),
        )
    return hashtag_list


def link_tags_to_post(post_id, tags):
    """
    It takes a post id and a list of tags, and links the tags to the post

    :param post_id: The id of the post you want to link the tags to
    :param tags: a list of strings
    """
    post = Post.objects.get(object_id=post_id)
    for tag in tags:
        _tag = Tag.objects.get(name=tag.lower())
        PostTag.objects.create(post=post, tag=_tag)


def object_id_generator(size, model, chars=string.ascii_letters + string.digits) -> str:
    """
    Generates and returns base64 call id
    """
    object_id = "".join(random.choice(chars) for _ in range(size))
    return check_object_id_exists(object_id=object_id, model=model)


def check_object_id_exists(object_id, model) -> str:
    """
    Checks if call id exists. Generates and returns new call id if exists
    """
    try:
        model.objects.get(object_id=object_id)
        new_object_id = object_id_generator()
        check_object_id_exists(object_id=new_object_id, model=model)
    except ObjectDoesNotExist:
        return object_id
