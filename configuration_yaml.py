import yaml


with open('config.yaml') as f:
    CONFIGURATION_YAML = yaml.load(f, Loader=yaml.FullLoader)


# Not having data types can also mutate the code in a bad way as seen below and in a real case scenario.

# However, while writing this I discovered that YAML files actually support data types https://realpython.com/python-yaml/. Here is an example utilizing them

"""
reviews:
  article_type: !!python/tuple
    - music
    - sports
  fields_to_translate:
    - title
    - pros_text
    - cons_text
    - text
descriptions: 
  article_type: !!python/tuple
    - design
  fields_to_translate:
    - content
"""


def format_sql_in_item(item, string: bool = True):
    return f"'{item}'" if string else str(item)


def query_article_type(items):
    if type(items) == list:
        return ','.join(format_sql_in_item(i) for i in items)
    else:
        return f"'{items}'"


class ArticleYaml:
    @classmethod
    def get_article_types(cls):
        return CONFIGURATION_YAML.get(cls.key).get('article_type')


class ReviewsYaml(ArticleYaml):
    key = 'reviews'


print(query_article_type(ReviewsYaml.get_article_types()))
# 'music','sports'


class DescriptionsYaml(ArticleYaml):
    key = 'descriptions'


print(query_article_type(DescriptionsYaml.get_article_types()))
# 'design'
