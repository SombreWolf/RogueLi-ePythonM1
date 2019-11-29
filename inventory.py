class Inventory:

    def __init__(self, size: int = -1):
        """
        
        :param size: The inventory's size
        """
        # {key: nb} where key is the name and nb the number of this item
        self.inventory = {}
        self.gold = 0
        self.slots = {'left hand': '-',
                      'right hand': '-',
                      'left jewel': '-',
                      'right jewel': '-',
                      'head': '-',
                      'chest': '-',
                      'pants': '-',
                      'arms': '-',
                      'legs': '-'}
        self.success = {}  # {"name of the success:[complete?,description]}
        self.len = len(self.inventory)
        self.isEmpty = (len(self.inventory) == 0)

    def sort(self) -> None:
        """
        Sort the inventory according to the alphabetical order
        """
        long = len(self.inventory)
        L = [self.inventory.popitem() for _ in range(long)]
        L.sort()
        self.inventory = {L[i][0]: L[i][1] for i in range(long)}

    def add(self, name: str, nb: int = 1) -> None:
        """
        Add an item to the inventory
        :param name: the name of the item
        :param nb: the number of item to add
        """

        # self.inventory.append((n, thing)) -> isn't a list
        # Pointer to thing: object -> doesn't work
        if name in self.inventory.keys():
            self.inventory[name] += nb

        if name not in self.inventory.keys():
            if self.isFull:
                pass
            else:
                self.inventory[name] = nb
                self.isFull = (self.size == len(self.inventory))
        self.len = len(self.inventory)
        self.isEmpty = (len(self.inventory) == 0)

    def take(self, name: str, nb: int = 1) -> None:
        """
        Delete "nb" times "name" from the inventory
        :param name: the item's name which is take from the inventory
        :param nb: the item's number which is take
        """
        if name in self.inventory.keys():
            if 0 <= nb <= self.inventory[name]:
                self.inventory[name] -= nb
                if self.inventory[name] == 0:
                    del self.inventory[name]
                    self.isEmpty = (len(self.inventory) == 0)
                    self.len = len(self.inventory)
            else:
                print('We have not enough ' + name)
        else:
            print('We have any ' + name)

    def __repr__(self) -> str:
        """
        Creates an image of the inventory
        :return: repr(self)
        """
        return self.__str__()

    def __str__(self) -> str:
        """
        Give the inventory as a string
        :return: ['nb1' x 'name1' ; 'nb2' x 'name2' ; ect... ]
        """
        if len(self.inventory) == 0:
            return 'Empty Inventory\n'
        else:
            txt = ''
            i = 1
            for key in self.inventory.keys():
                txt = ' \n' + txt \
                      + '(' + str(i) + ') ' \
                      + str(self.inventory[key]) + ' x ' \
                      + key + '\n'
                i += 1
            return txt

    def sold_aff(self):
        """
        Give an specific image of inventory for the merchant's interface
        :return: [(1) 'nb1' x 'name1' ; (2) 'nb2' x 'name2' ; ect... ]
        """
        if len(self.inventory) == 0:
            return 'Nothing'
        else:
            aff = ''
            i = 1
            for key in self.inventory.keys():
                aff = ' \n' + aff \
                      + '(' + str(i) + ') ' \
                      + str(self.inventory[key]) + ' x ' \
                      + key + '\n'
                i += 1
            return aff + '\n'

