import json

from willie import web
from willie.module import commands

UD_URL = 'http://api.urbandictionary.com/v0/define?term='


def get_def(word, num=0):
    url = UD_URL + word
    resp = json.loads(web.get(url))
    nom = num + 1
    if resp['result_type'] == 'no_results':
        definition = 'Definition %s not found!' % (word)
    else:
        try:
            item = resp['list'][num]['definition']
            total_nom = len(resp['list'])
            definition = '(%s/%s) %s' % (nom, total_nom, item)
        except IndexError:
            definition = ('Definition entry %s does'
                          'not exist for \'%s\'.' % (nom, word))
    return definition


@commands('urban')
def urban(bot, trigger):
    args = trigger.group(2).split(' ')
    defnum = 0
    word = ' '.join(args)
    if len(args) > 1:
        try:
            defnum = int(args[0])
            defnum = defnum - 1
            word = ' '.join(args[1:])
        except ValueError:
            pass
    definition = get_def(word, defnum)
    bot.say(definition, max_messages=5)
