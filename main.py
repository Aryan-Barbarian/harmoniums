import world
from PIL import Image
SCALE = 10
def state_to_image(state):
	width = state["width"]
	entity_states = state["entities"]
	sound_strength = state["sound_strength"]

	img = Image.new('RGB', (width, width))
	img_data = img.load()

	for x in xrange(width):
		for y in xrange(width):
			sound_val = sound_strength[(x,y)]
			rate = int(min(1, sound_val / 50)*255)
			img_data[x,y] = (rate, rate, rate)

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

	img = img.resize( (width*SCALE, width*SCALE))
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
	wrld.add_entity(world.SimpleHarmonium(), 25, 10) # add a harmonium 
	wrld.add_entity(world.SimpleHarmonium(), 25, 25) # add a harmonium close

	TURNS = 4000
	jump = 8
	for i in xrange(TURNS):
		wrld.turn()
		if i % jump == 0:
			state = wrld.get_state()
			image = state_to_image(state) # maybe edit image
			image.save("test_{}.png".format(str(i).zfill(4)), "PNG")

if __name__ == "__main__":
	main()