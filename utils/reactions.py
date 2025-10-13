"""
Utility functions for handling reactions (likes/dislikes).

This module provides reusable functions for managing likes and dislikes
on different types of content (apps, comments, news, etc.).
"""

from typing import Dict, Tuple, Type
from django.db import models, transaction
from django.core.cache import cache


def get_reaction_counts(
    model: Type[models.Model],
    object_id: int,
    like_model: Type[models.Model],
    dislike_model: Type[models.Model],
    cache_timeout: int = 300,
) -> Dict[str, int]:
    """
    Get like and dislike counts for an object with caching.

    Args:
        model: The model class of the object
        object_id: ID of the object
        like_model: Model class for likes
        dislike_model: Model class for dislikes
        cache_timeout: Cache timeout in seconds (default: 5 minutes)

    Returns:
        Dictionary with 'likes' and 'dislikes' counts
    """
    cache_key = f"{model.__name__}_{object_id}_reactions"
    cached_data = cache.get(cache_key)

    if cached_data:
        return cached_data

    # Get field name for the foreign key (e.g., 'app', 'comment', 'news')
    field_name = model.__name__.lower().replace("model", "")
    filter_kwargs = {f"{field_name}_id": object_id}

    counts = {
        "likes": like_model.objects.filter(**filter_kwargs).count(),
        "dislikes": dislike_model.objects.filter(**filter_kwargs).count(),
    }

    cache.set(cache_key, counts, cache_timeout)
    return counts


def handle_reaction(
    ip: str,
    object_id: int,
    reaction_type: str,
    like_model: Type[models.Model],
    dislike_model: Type[models.Model],
    field_name: str,
) -> Tuple[bool, Dict[str, int]]:
    """
    Handle a like or dislike reaction with optimized queries.

    This function implements a toggle behavior:
    - If user likes and already liked: do nothing
    - If user likes but already disliked: remove dislike, add like
    - If user dislikes and already disliked: do nothing
    - If user dislikes but already liked: remove like, add dislike

    Args:
        ip: User's IP address
        object_id: ID of the object being reacted to
        reaction_type: Either 'like' or 'dislike'
        like_model: Model class for likes
        dislike_model: Model class for dislikes
        field_name: Name of the foreign key field (e.g., 'app', 'comment')

    Returns:
        Tuple of (success: bool, counts: dict)
    """
    filter_kwargs = {"ip": ip, f"{field_name}_id": object_id}
    create_kwargs = {"ip": ip, f"{field_name}_id": object_id}

    with transaction.atomic():
        if reaction_type == "like":
            # Check if already liked
            if like_model.objects.filter(**filter_kwargs).exists():
                # Already liked, do nothing
                pass
            else:
                # Remove dislike if exists, then add like
                dislike_model.objects.filter(**filter_kwargs).delete()
                like_model.objects.create(**create_kwargs)

        elif reaction_type == "dislike":
            # Check if already disliked
            if dislike_model.objects.filter(**filter_kwargs).exists():
                # Already disliked, do nothing
                pass
            else:
                # Remove like if exists, then add dislike
                like_model.objects.filter(**filter_kwargs).delete()
                dislike_model.objects.create(**create_kwargs)

        # Get updated counts
        counts = {
            "likes": like_model.objects.filter(**{f"{field_name}_id": object_id}).count(),
            "dislikes": dislike_model.objects.filter(**{f"{field_name}_id": object_id}).count(),
        }

        # Invalidate cache
        from django.apps import apps

        model_class = apps.get_model("applications", field_name.capitalize() + "Model")
        cache_key = f"{model_class.__name__}_{object_id}_reactions"
        cache.delete(cache_key)

        return True, counts


def check_user_reaction(
    ip: str, object_id: int, like_model: Type[models.Model], dislike_model: Type[models.Model], field_name: str
) -> Dict[str, bool]:
    """
    Check if a user has liked or disliked an object.

    Args:
        ip: User's IP address
        object_id: ID of the object
        like_model: Model class for likes
        dislike_model: Model class for dislikes
        field_name: Name of the foreign key field

    Returns:
        Dictionary with 'has_liked' and 'has_disliked' boolean values
    """
    filter_kwargs = {"ip": ip, f"{field_name}_id": object_id}

    return {
        "has_liked": like_model.objects.filter(**filter_kwargs).exists(),
        "has_disliked": dislike_model.objects.filter(**filter_kwargs).exists(),
    }
