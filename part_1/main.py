from models import Quote


def all_author_quotes(author: str):
    result = []
    for quote in Quote.objects:
        if quote.author.fullname.lower() == author:
            result.append(quote.to_mongo().to_dict())
    return result


def find_tag(tag: str):
    result = []
    quotes = Quote.objects(tags__icontains=tag)
    for quote in quotes:
        result.append(quote.to_mongo().to_dict())
    return result


def find_tags(tags: str):
    result = []
    tags = tags.lower().strip().split(',')
    quotes = Quote.objects(tags__in=tags)
    for quote in quotes:
        result.append(quote.to_mongo().to_dict())
    return result


COMMANDS = {
    'name': all_author_quotes,
    'tag': find_tag,
    'tags': find_tags
}


def command_parser(message: str):
    try:
        command, data = message.lower().split(':')
    except ValueError as error:
        return f'Error: {error}'
    if command.strip() in COMMANDS.keys():
        return COMMANDS.get(command.strip())(data.strip())
    else:
        return 'Wrong command! Try again'


def main():
    while True:
        input_message = input('>>> ')
        if input_message.lower() == 'exit':
            break
        print(command_parser(input_message))


if __name__ == '__main__':
    main()
