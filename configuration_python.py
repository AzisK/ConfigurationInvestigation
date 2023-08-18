CONFIGURATION = {
    'reviews': {
        'article_type': tuple('music sports'.split()),
        'fields_to_translate': tuple('title pros_text const_text text'.split()),
    },
    'descriptions': {
        'article_type': tuple('design'.split()),
        'fields_to_translate': tuple('content'.split()),
    }
}


def format_sql_in_item(item, string: bool = True):
    return f"'{item}'" if string else str(item)


def sql_in(iterable, string: bool = True) -> str:
    return ','.join([format_sql_in_item(item, string) for item in iterable])


class ArticlePython:
    @classmethod
    def get_article_types(cls):
        return CONFIGURATION.get(cls.key).get('article_type')


class Reviews(ArticlePython):
    key = 'reviews'


print(sql_in(Reviews.get_article_types()))
# 'music','sports'


class Descriptions(ArticlePython):
    key = 'descriptions'


print(sql_in(Descriptions.get_article_types()))
# 'design'


# Another way is to structure everything in within classes


class ArticleClass:
    @classmethod
    def get_article_types(cls):
        return cls.article_types


class ReviewsConfig(ArticleClass):
    article_types = tuple('music sports'.split())


print(sql_in(ReviewsConfig.get_article_types()))
# 'music','sports'


class DescriptionsConfig(ArticleClass):
    article_types = tuple('design'.split())


print(sql_in(DescriptionsConfig.get_article_types()))
# 'design'


# We can use composition over inheritance to have even more flexibility


from typing import Tuple
from dataclasses import dataclass


@dataclass
class ArticleComposition:
    article_types: Tuple


descriptions = ArticleComposition(article_types=tuple('design'.split()))
print(sql_in(descriptions.article_types))
# 'design'


# Let us now imagine that hacker wants us to focus and write about fashion and he changes the article type to fashion


fashions = ArticleComposition(article_types='fashion')
print(sql_in(fashions.article_types))
# 'f','a','s','h','i','o','n'

descriptions.article_types = 'fashion'
print(sql_in(descriptions.article_types))
# 'f','a','s','h','i','o','n'

# We can see that he can easily do it and even pass a wrong data type
# Using dataclasses we can also freeze the class variables


from typing import Tuple
from dataclasses import dataclass


@dataclass(frozen=True)
class ArticleFrozen:
    article_types: Tuple


reviews = ArticleFrozen(article_types=tuple('music sports'.split()))
print(sql_in(reviews.article_types))
# 'music','sports'


# reviews.article_types = 'fashion'
# dataclasses.FrozenInstanceError: cannot assign to field 'article_types'


# To my mind, in the end it can be a mix of Python configuration and some of it can already live in the class. Python can provide more structure even though YAML configuration can also work. Another disadvantage not discussed here is the I/O operation of reading the YAML file which adds overhead and complexity to the application

# We can also have custom data types in side data types. This way we can nest logic in its own scope as well as still have a strong hinting support.

# Below we utilize namedtuples as config inside dataclasses


from typing import NamedTuple
from typing import Tuple


class ArticleTupleConfig(NamedTuple):
    article_types: Tuple
    fields_to_translate: Tuple


reviews_config = ArticleTupleConfig(
    tuple('music sports'.split()),
    tuple('title pros_text cons_text text'.split()),
)

descriptions_config = ArticleTupleConfig(
    tuple('design'.split()),
    tuple('content'.split()),
)


from dataclasses import dataclass


@dataclass(frozen=True)
class ArticleFrozenWithNamedTuples:
    config: ArticleTupleConfig


reviews_with_named_tuple = ArticleFrozenWithNamedTuples(reviews_config)
print(sql_in(reviews_with_named_tuple.config.article_types))
# 'music','sports'
print(sql_in(reviews_with_named_tuple.config.fields_to_translate))
# 'title','pros_text','cons_text','text'


descriptions_with_named_tuple = ArticleFrozenWithNamedTuples(descriptions_config)
print(sql_in(descriptions_with_named_tuple.config.article_types))
# 'design'
print(sql_in(descriptions_with_named_tuple.config.fields_to_translate))
# 'content'
