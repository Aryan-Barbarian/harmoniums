import world
from PIL import Image

def state_to_image(state):
	width = state["width"]
	entity_states = state["entities"]

	img = Image.new('RGB', (width, width))
	img_data = img.load()

	for entity in entity_states:
		name = entity["name"]
		x,y = entity["location"]
		newcolor = None
		if name == "soundsource":
			if entity["playing"]:
				newcolor = (50,50,50)
		elif name == "harmonium":
			if entity["is_alive"]:
				newcolor = (100, 68, 255)
			else:
				newcolor = (255, 187, 0)

		if newcolor is not None:
			img_data[x,y] = newcolor

	return img

def state_to_text(state):
	width = state["width"]
	entity_states = state["entities"]
	data = [ [ " " for col in xrange(width)] for row in xrange(width)]
	for entity in entity_states:
		name = entity["name"]
		x,y = entity["location"]
		newcolor = None
		if name == "soundsource":
			data[x][y] = "&"
		elif name == "harmonium":
			if entity["is_alive"]:
				data[x][y] = "O"
			else:
				data[x][y] = "X"

	toprint = "\n".join(["".join(row) for row in data])
	return toprint

def main():
	WIDTH = 40
	wrld = world.World(WIDTH) # TODO: args
	wrld.add_entity(world.SoundSource(), 30, 30) # add a sound source at (30, 30)
	wrld.add_entity(world.SimpleHarmonium(), 25, 30) # add a harmonium 
	wrld.add_entity(world.SimpleHarmonium(), 29, 30) # add a harmonium close

	TURNS = 20

	for i in xrange(TURNS):
		wrld.turn()
		state = wrld.get_state()
		# print(state_to_text(state))
		# print(state)
		print("*"*WIDTH)
		image = state_to_image(state) # maybe edit image
		image.save("test_{}.png".format(i), "PNG")

if __name__ == "__main__":
	main()