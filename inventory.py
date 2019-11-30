class Inventory:

    def __init__(self, inventory={}, gold=0, success={"First Game":[True, "Launch your first game"], "Killer":[False, "Kill 50 monsters"]}):
        """
        :param size: The inventory's size
        """
        # {key: nb} where key is the name and nb the number of this item
        self.inventory = inventory
        self.gold = gold
        self.slots = {'left hand': '-',
                      'right hand': '-',
                      'left jewel': '-',
                      'right jewel': '-',
                      'head': '-',
                      'chest': '-',
                      'pants': '-',
                      'arms': '-',
                      'legs': '-'}
        self.success = success # {"name of the success:[complete?,description]}

    def sort(self) -> None:
        """
        Sort the inventory according to the alphabetical order
        :return:
        """
        long = len(self.inventory)
        L = [self.inventory.popitem() for _ in range(long)]
        L.sort()
        self.inventory = {L[i][0]: L[i][1] for i in range(long)}

    def show(self):
        """
        function to show the inventory
        :return:
        """
        items = []
        if len(self.inventory) == 0:
            print("Your inventory is empty")

        else:
            for i in list(self.inventory.keys()):
                items.append(i)
                print(str(items.index(i)+1) + ")" + i.name + " (x" + str(self.inventory[i]) + ")")

        print("Golds : " + str(self.gold))
        return items
