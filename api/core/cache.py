from django.core.cache import cache


class CacheMixin:

    cache_prefix = ''

    def get_cached_data(self, request,
                        prefix,
                        queryset,
                        page,
                        serializer_class,
                        paginated_response):
        self.cache_prefix = prefix
        cache_key = f'{self.cache_prefix}{request.get_full_path().replace('/', '_')
        .replace('?', '_')
        .replace('&', '_')
        .replace('=', '_')}'

        data = cache.get(cache_key)
        if data:
            return data

        if page is not None:
            serializer = serializer_class(instance=page, many=True, context={'request': request})
            data = paginated_response(serializer.data).data
        else:
            serializer = serializer_class(instance=queryset, many=True, context={'request': request})
            data = serializer.data
        cache.set(cache_key, data, 120)
        return data