import random
import string

from django.db.models.base import Model

from core.posts.models import Post, PostTag, Tag


def forbidden_attributes() -> list[str]:
    return [
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


def extract_hashtags(text: str) -> list[str]:
    """
    function to extract all the hashtags in a product description.
    It generates new `Tag` instance, if it does not exist, for each of
    of the tags
    """
    hashtag_list = []

    for word in text.split():
        if word[0] == "#":
            hashtag_list.append(word[1:])

    for hashtag in hashtag_list:
        obj, created = Tag.objects.get_or_create(
            name=hashtag.lower(),
        )
    return hashtag_list


def link_tags_to_post(post_id: str, tags: list) -> None:
    post = Post.objects.get(object_id=post_id)
    for tag in tags:
        _tag = Tag.objects.get(name=tag.lower())
        PostTag.objects.create(post=post, tag=_tag)


def object_id_generator(
    size: int, model: Model, chars: str = string.ascii_letters + string.digits
) -> str:
    """
    Generates and returns base64 call id
    """
    object_id = "".join(random.choice(chars) for _ in range(size))
    return check_object_id_exists(object_id=object_id, model=model)


def check_object_id_exists(object_id: str, model: Model) -> str:
    """
    Checks if call id exists. Generates and returns new call id if exists
    """
    try:
        model.objects.get(object_id=object_id)
        new_object_id = object_id_generator()
        check_object_id_exists(object_id=new_object_id, model=model)
    except model.DoesNotExist:
        return object_id
