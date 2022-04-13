import time

from models.item import Item

i = Item.create("fishing rod")
print(i)
print(repr(i))
