

# Filter
class Filter:
    def __init__(self, title: str, sort: str, order: int, skip: int, take: int):
        self.title = title
        self.sort = sort
        self.order = order
        self.skip = skip
        self.take = take

    @staticmethod
    def create(raw_filter: dict):
        return Filter(
            title=raw_filter.get('title', ''),
            sort=raw_filter.get('sort', 'title') if raw_filter.get(
                'sort', '') != '' else 'filter',
            order=raw_filter.get('order', 1),
            skip=raw_filter.get('skip', 0),
            take=raw_filter.get('take', 0)
        )
