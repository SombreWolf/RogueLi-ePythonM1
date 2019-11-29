import game as g
import character as char
import inventory as inv
import item as it

if __name__ == '__main__':
    game = g.Game()
    monster = char.Character("Mob", "Monster", inventory=inv.Inventory(inventory={it.Equipment("かたな", "Just a saber", "Weapon"):1}, gold=10))
    merchant = char.Character("Bobby", "Merchant", inventory=inv.Inventory(inventory={it.Equipment("かたな", "Just a saber", "Weapon"):1}, gold=10))
    game.fight(game.player, monster)
    game.inventory_view(game.)
