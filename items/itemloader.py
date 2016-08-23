import os
import random
import logging
from importlib.machinery import SourceFileLoader

logger = logging.getLogger('rg')

def load_item(name, buff):
	path = 'items/{0}/{1}.py'.format(buff, name)

	if not os.path.exists(path):
		return None

	item_loader = SourceFileLoader(name, path)
	item = item_loader.load_module()

	return check_item(item, name, buff)

def check_item(item, name, buff):
	item.code_name = name
	item.buff = buff

	required = [ 'name', 'description', 'price' ]

	for r in required:
		if not hasattr(item, r):
			logger.warn('Item "{0}" has no attribute {1}!'.format(name, r))
			return None

	defaults = [
		( lambda *args: None, [ 'on_room', 'on_enemy', 'on_escape', 'on_corridor', 'on_shop', 'on_pray', 'on_buy', 'on_dice', 'on_use' ] ), # callbacks
		( lambda *args: 0, [ 'get_dice_bonus', 'get_damage_bonus', 'fight_use' ]),
		( 0, [ 'damage', 'mana_damage', 'charisma', 'intelligence', 'defence' ] ), # buffs
		( '', [ 'aura' ] ), # eeeh. meh
		( [ ], [ 'tags', 'loot' ] ), # some arrays?
		( False, [ 'usable', 'fightable', 'iscursed' ])
	]

	for def_val, names in defaults:
		for name in names:
			if not hasattr(item, name):
				setattr(item, name, def_val)

	return item

def load_random_item(buff):
	pth = 'items/' + buff + '/'
	items =  [ f[:-3] for f in os.listdir(pth) if f.endswith('.py') ]

	return (buff, random.choice(items))

def load_shop_items():
	items = [
		load_random_item('bad'),
		load_random_item('good'),
		load_random_item('neutral')
	]

	random.shuffle(items)

	return items
