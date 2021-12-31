from time import time, sleep
from re import sub


class Fish():

    TIMEOUT = 15
    CAPTURED = None
    NAME = None
    BALL = 'Pokeballs'  # default one in order to send greatballs

    LEGENDARYS = [
        # Gen I
        # Gen II
        "Suicune",
        # Gen III
        "Kyogre",
        # Gen IV
        "Palkia",
        "Phione",
        "Manaphy",
        # Gen V
        "Keldeo",
        "Volcanion",
        # Gen VI
        # Gen VII
        "Tapu Fini",
        # Gen VIII
        "Urshifu"
    ]

    def __init__(self, bag, driver):
        self.DRIVER = driver
        self.BAG = bag
        self.spawned, self.message, self.name = self.spawn(time())
        if self.spawned:
            self.which_ball()
            self.CAPTURED = '\nCongratulations' in self.message.text
            # False because not earning Pokecoins
            self.BAG.update_balls(self.message.text, False)

    def spawn(self, START_TIME):
        message = self.DRIVER.WaitNew(
            ';fish', f'{ self.DRIVER.USERNAME } cast')
        bak_txt = message.text
        while time() < START_TIME + self.TIMEOUT and bak_txt == message.text:
            sleep(0.1)
        if 'PULL' in message.text:  # there is a fish
            print("Trying to pull")
            self.DRIVER.WaitChangesOnMessage('pull', message)
            if 'got away' in message.text:
                return False, message, ''
            return True, message, sub(r'(.|\n)*?a wild (.*)!(.|\n)*', r'\2', message.text)
        elif 'got away' in message.text:
            return False, message, ''
        else:
            return None, message, ''

    def which_ball(self) -> None:
        if 'Shiny' in self.message.text or 'Golden' in self.message.text or any(contain in self.message.text for contain in self.LEGENDARYS):
            self.BALL = 'Masterballs'

        return self.DRIVER.WaitChangesOnMessage(self.BAG.BALLS[self.BALL]['call'], self.message)

    def __repr__(self):
        return f"""It's a { self.name }, {'and is now in you PC !' if self.CAPTURED else 'ran away.'}""" if self.name else 'No Fish to see here.'
