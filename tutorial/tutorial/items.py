from datetime import datetime
from scrapy.item import Item, Field
from scrapy.loader.processors import (
    MapCompose,
    TakeFirst
)


def remove_quotes(text):
    return text[1: -1]


def convert_date(text):
    return str(datetime.strptime(text, '%B %d, %Y'))


def parse_location(text):
    return text[3:]


class QuoteItem(Item):
    quote_content = Field(
        input_processor=MapCompose(remove_quotes),
        output_processor=TakeFirst()
    )

    author_name = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )

    author_birthday = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )

    author_bornlocation = Field(
        input_processor=MapCompose(parse_location),
        output_processor=TakeFirst()
    )

    author_bio = Field(
        input_processor=MapCompose(str.strip),
        output_processor=TakeFirst()
    )

    tags = Field()
