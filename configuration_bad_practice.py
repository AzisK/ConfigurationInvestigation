# File 1
def magic_config_load(obj):
    return obj

# It is a bad choice to call any method magic


def dummy():
    ...


config = magic_config_load(dummy)

# We are using dummy methods to load the YAML file

TRANSL_CFG = config.translation
LANG_CFG = config.languages
ELASTIC_CFG = config.elastic
HTTP_CFG = config.http

DEBUG_MODE = True


# File 2
class CookingV2Client:
    ...


client = CookingV2Client(**HTTP_CFG.client['cooking'])

# CookingV2Client can already know that it has to use `cooking` client, we don't need to tell it. Any other value would also be a mistake


# File 3
class CarReviewTranslationEtl:
    debug_mode = True
    model = 'reviews'
    vertical = 'car'
    brand = 'kayak'
    batch_size = 1


class ReviewsTranslateCooking:
    @property
    def serializer(self):
        return CookingSerializer(**TRANSL_CFG.models[self.model], target_lang=self.target_lang)


# ReviewsTranslateCooking can already know it has to use 'reviews' model, we don't need to tell it.  Any other value would also be a mistake
