from django.core.cache import cache
from blog.models import Blog
from main_app.settings import CACHE_ENABLED


def get_blogs_from_cache():
    if not CACHE_ENABLED:
        return Blog.objects.filter(is_published=True)

    key = 'published_blogs_list'
    posts = cache.get(key)
    if posts is not None:
        return posts

    posts = Blog.objects.filter(is_published=True)
    cache.set(key, posts, timeout=60 * 15)  # Кешируем на 15 минут
    return posts
