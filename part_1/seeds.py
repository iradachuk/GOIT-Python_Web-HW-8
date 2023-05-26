import json

from part_1.models import Quote, Author

with open('authors.json', encoding='utf-8') as file:
    authors = json.load(file)
    for author in authors:
        Author(**author).save()

with open('quotes.json', encoding='utf-8') as file:
    quotes = json.load(file)
    for quote in quotes:
        author = Author.objects(fullname=quote.pop('author')).first()
        Quote(author=author, **quote).save()

