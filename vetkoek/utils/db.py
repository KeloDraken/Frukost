from datetime import datetime
from math import log

from django.db.models import Model
from django.http import HttpResponseBadRequest

from vetkoek.core.accounts.models import User
from vetkoek.core.posts.models import Post


def epoch_seconds(date) -> float:
    """
    Calculates the time past since unix epoch
    """
    epoch = datetime(1970, 1, 1)
    min_time = datetime.min.time()
    td = datetime.combine(date, min_time) - epoch
    return td.days * 86400 + td.seconds + (float(td.microseconds) / 1000000)


def score(ups: int, downs: int) -> int:
    """
    Sums upvotes and downvotes
    """
    return ups + downs


def hot(ups: int, downs: int, date) -> float:
    """
    "The hot formula. It's the
    same as the Reddit hot formula."

    :param ups: the number of upvotes the post has received
    :param downs: The number of downvotes the post has received
    :param date: The date and time of the submission
    :return: The hotness of a post.
    """
    s = score(ups, downs)
    order = log(max(abs(s), 1), 10)
    sign = 1 if s > 0 else -1 if s < 0 else 0
    seconds = epoch_seconds(date) - 1134028003
    return round(sign * order + seconds / 45000, 7)


def check_has_user_voted(model: Model, user: User, post: Post):
    """
    If the user has voted on the post, return True, otherwise return False

    :param model: The model that you want to check if the user has voted on
    :param user: The user who is voting
    :param post: The post object
    :return: True or False
    """
    try:
        model.objects.get(user=user, post=post)
        return True
    except model.DoesNotExist:
        return False


def cast_vote(post, vote_value, vote):
    """
    If the user upvotes, add 1 to the upvotes, add the score to the post score, and save the vote. If the user downvotes,
    add 1 to the downvotes, subtract the score from the post score, and save the vote. If the user cancels their vote,
    subtract 1 from the upvotes or downvotes, subtract the score from the post score, and save the vote

    :param post: The post that the user is voting on
    :param vote_value: 1 for upvote, -1 for downvote, 0 for cancel vote
    :param vote: The vote object
    :return: the HttpResponseBadRequest()
    """
    vote.has_voted = True
    # Upvote
    if vote_value == 1:
        vote.value = vote_value
        post.upvotes = post.upvotes + 1

        # Calculate score
        age = post.date_created
        score = hot(ups=post.upvotes, downs=post.downvotes, date=age)
        post.score = post.score + score
        post.save()
        vote.save()
    # Downvote
    elif vote_value == -1:
        vote.value = vote_value
        post.downvotes = post.downvotes + 1

        # Calculate score
        age = post.date_created
        score = hot(ups=post.upvotes, downs=post.downvotes, date=age)
        post.score = post.score - score

        post.save()
        vote.save()
    # Cancel vote
    elif vote_value == 0:
        # If user previously downvoted the post
        if vote.value == -1:
            vote.value = 0
            post.downvotes = post.downvotes - 1

            # Calculate score
            age = post.date_created
            score = hot(ups=post.upvotes, downs=post.downvotes, date=age)
            post.score = post.score - score

            post.save()
            vote.save()

        # If user previously upvoted the post
        elif vote.value == 1:
            vote.value = 0
            post.upvotes = post.upvotes - 1

            # Calculate score
            age = post.date_created
            score = hot(ups=post.upvotes, downs=post.downvotes, date=age)
            post.score = post.score - score

            post.save()
            vote.save()
        elif vote.value == 0:
            pass

    else:
        return HttpResponseBadRequest()
