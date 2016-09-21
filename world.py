
class World(object):
	
	"""World stores all entities and handles their actions"""
	def __init__(self, width):
		self.width = width
		self.entities = set() # all world entities
		self.sound_strength = dict() # { (x, y) => sound strength }
		self.loc_to_entities = dict()
		self.entity_to_loc = dict()
	
	def get_state(self):
		entity_states = []
		for entity in self.entities:
			entity_state = entity.get_state()
			entity_states.append(entity_state)
		return {"width" : self.width,
				"sound_strength" : self.sound_strength,
				"entities" : entity_states}

	
	def add_entity(self, entity, locx, locy):
		self.entities.add(entity)
		entity.world = self
		self.move_entity(entity, locx, locy)

	def get_location(self, entity):
		return self.entity_to_loc.get(entity, None)

	def move_entity(self, entity, newx, newy):
		old_loc = self.get_location(entity)
		if old_loc is not None:
			self.loc_to_entities[old_loc].remove(entity)

		new_loc = (newx, newy)
		if new_loc not in self.loc_to_entities:
			self.loc_to_entities[new_loc] = set()
		self.loc_to_entities[new_loc].add(entity)

		self.entity_to_loc[entity] = new_loc

	def add_sound(self, locx, locy, sound_val):
		loc_key = (locx, locy)
		self.sound_strength[loc_key] = self.sound_strength.get(loc_key, 0) + sound_val

	def get_energy(self, locx, locy):
		return self.sound_strength.get((locx, locy), 0)

	def turn(self):
		actions = [] # [ (actor, action) ... ]
		for entity in self.entities:
			action = entity.turn()
			entity.handle_action(action)
			if action is not None:
				actions.append((entity, action)) 

	def valid_location(self, locx, locy):
		if locx < 0 or locx >= self.width:
			return False
		if locy < 0 or locy >= self.width:
			return False
		return True


######################################################
############## VARIOUS ENTITY CLASSES ################
######################################################

class Entity(object):
	"""docstring for Entity"""
	def __init__(self):
		super(Entity, self).__init__()

	def get_action(self):
		return None;

	def turn(self):
		action = self.get_action()
		return action

	def handle_action(self, action):
		pass;

	def get_name(self):
		return "entity"

	def get_location(self):
		if self.world is not None:
			return self.world.get_location(self)
		return None

	def get_state(self):
		state = {"name" : self.get_name()}
		location = self.get_location()
		if location is not None:
			state["location"] = location
		return state

class SoundSource(Entity):

	def __init__(self):
		super(SoundSource, self).__init__()
		self.playing = False
		self.strength = 10

	def get_action(self):
		if not self.playing:
			return "start"

	def get_name(self):
		return "soundsource"

	def handle_action(self, action):
		modifier = 0
		if action == "start":
			self.playing = True
			modifier = 1
		elif action == "stop":
			self.playing = False
			modifier = -1

		if modifier != 0:
			x, y = self.get_location()
			width = self.world.width
			for otherx in xrange(width):
				dx2 = (x - otherx)**2
				for othery in xrange(width):
					dy2 = (y - othery)**2
					to_add = float(self.strength) / max(0.00001, (dx2 + dy2))
					self.world.add_sound(modifier*otherx, othery, to_add)

	def get_state(self):
		state = super(SoundSource, self).get_state()
		state["playing"] = self.playing
		state["strength"] = self.strength
		return state

class SimpleHarmonium(Entity):
	"""docstring for SimpleHarmonium"""
	def __init__(self):
		super(SimpleHarmonium, self).__init__()
		self.current_energy = 5
		self.is_alive = True

	def is_unhappy(self):
		return self.current_energy < 0

	def turn(self):
		action = super(SimpleHarmonium, self).turn()
		x, y = self.get_location()
		self.current_energy += self.world.get_energy(x, y) - 1
		return action

	def get_action(self):
		if not self.is_alive:
			return None
		if self.current_energy <= -10:
			return "die"
		if self.is_unhappy():
			potential_gains = self.get_neighbor_vals() # {[up/down/left/right] => diff in sound_val}
			best = (0, None) # Will go after any improvement because 0
			for change, gain in potential_gains.items():
				if gain > best[0]:
					best = gain, change
			if best[1] is not None:
				return "move {}".format(best[1])

		elif self.current_energy >= 20:
			return "flake"
		else:
			return "sit"

	def get_neighbor_vals(self):
		x,y = self.get_location()
		curr_rate = self.world.get_energy(x,y)
		gains = dict()
		gains["up"] = self.world.get_energy(x, y+1) - curr_rate
		gains["down"] = self.world.get_energy(x, y-1) - curr_rate
		gains["left"] = self.world.get_energy(x-1, y) - curr_rate
		gains["right"] = self.world.get_energy(x+1, y) - curr_rate
		return gains

	def handle_action(self, action):

		x, y = self.get_location()
		newx, newy = x,y

		if action is None:
			return
		elif action == "move left":
			newx -= 1
		elif action == "move right":
			newx += 1
		elif action == "move down":
			newy -= 1
		elif action == "move up":
			newy += 1
		elif action == "flake":
			pass;
		elif action == "sit":
			pass;
		elif action == "die":
			self.is_alive = False
		
		if (x != newx or y != newy):
			self.world.move_entity(self, newx, newy)

	def get_name(self):
		return "harmonium"

	def get_state(self):
		state = super(SimpleHarmonium, self).get_state()
		state["current_energy"] = self.current_energy
		state["is_alive"] = self.is_alive
		return state
		