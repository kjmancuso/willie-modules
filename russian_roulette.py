#   Copyright 2011,2014 Jason Kölker
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import time

try:
    import randomdotorg
    random = randomdotorg.RandomDotOrg()
except ImportError:
    import random

from willie.module import commands, NOLIMIT, rate


class RussianRoulette(object):
    """Provide access to dice games"""

    def __init__(self, *args, **kwargs):
        super(RussianRoulette, self).__init__(*args, **kwargs)
        self.game = None
        self.gametime = time.time()

    def _gun(self, size=6):
        chamber = [0] * (size - 1)
        chamber.append(1)
        random.shuffle(chamber)
        return chamber

    def play(self):
        if not self.game:
            self.game = self._gun()

        self.gametime = time.time()
        return self.game.pop()


CHANNELS = {}
EXPIRATION = 86400
BANG = 'LOL BANG!'
CLICK = 'click'
WUSS = 'Come on man, you dietz?'
THORN = 'http://i.imgur.com/fNE4h.jpg'


def game(channel):
    if channel not in CHANNELS:
        CHANNELS[channel] = RussianRoulette()

    suicide = CHANNELS[channel]

    for key, value in CHANNELS.copy().iteritems():
        if time.time() - value.gametime > EXPIRATION:
            del CHANNELS[key]

    return suicide


def say(bot, msg):
    padding = ' ' * random.randint(0, 20)
    bot.say(msg + padding)


@rate(1)
@commands('russian')
def roulette(bot, trigger, **kwargs):
    suicide = game(trigger.sender)
    params = trigger.group(2)
    if params:
        cmd = params.split(' ', 1)[0].lower()

        if cmd == 'play':
            if suicide.play() == 1:
                result = BANG
                suicide.game = None

            else:
                result = CLICK

        elif cmd == 'wuss':
            result = WUSS
            suicide.game = None

        elif cmd == 'thorn':
            result = THORN

    else:
        result = """Play russian roulette:
                    play the game: .russian play
                    stop the game: .russian wuss
                 """

    amiop = bot.sub('$nickname') in bot.ops[trigger.sender]
    if result == BANG and trigger.sender[0] == '#' and amiop:
        pnick = [row for row in bot.privileges[trigger.sender]
                 if trigger.nick in row]
        if str(pnick)[7] == '!':
            bot.reply('LOL BANG!!!! huehuehuehuehue')
        else:
            bot.write(['KICK', trigger.sender, trigger.nick, BANG])
    else:
        say(bot, result)

    return NOLIMIT
