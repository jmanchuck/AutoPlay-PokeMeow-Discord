from re import sub
from .CustomDriver import CustomDriver


class Pokemon():

    RARITYS = {
        "Legendary":   "mb",
        "Shiny":   "mb",
        "Super Rare":    "ub",
        "Rare":    "gb",
        "Uncommon":     "pb",
        "Common":     "pb"
    }

    CAPTURED = False

    def __init__(self, bag, driver) -> None:
        self.DRIVER: CustomDriver = driver
        self.BAG = bag
        self.message, self.rarity, self.name = self.spawn()

        self.CAPTURED = self.which_ball()

    def __repr__(self) -> str:
        return f"""It's a {self.name}, it's rarity is {self.rarity}, {'and is now in you PC !' if self.CAPTURED else 'ran away.'}"""

    def spawn(self):
        message = self.DRIVER.WaitNew(';p', f"{ self.DRIVER.USERNAME } found")
        return (message,
                sub(r'(.|\n)*?a wild .*!\n(.*) \((.|\n)*', r'\2', message.text),
                sub(r'(.|\n)*?a wild (.*)!(.|\n)*', r'\2', message.text))

    def which_ball(self) -> None:
        return self.DRIVER.WaitChangesOnMessage(self.RARITYS.get(self.rarity), self.message)
