import world

def state_to_image(state):
	img = None
	return img

def main():
	wrld = world.World(100) # TODO: args
	wrld.add_entity(world.SoundSource(), 30, 30) # add a sound source at (30, 30)
	wrld.add_entity(world.SimpleHarmonium(), 20, 30) # add a harmonium 
	wrld.add_entity(world.SimpleHarmonium(), 29, 30) # add a harmonium close

	TURNS = 20
	frames = []

	for i in xrange(TURNS):
		wrld.turn()
		state = wrld.get_state()
		image = state_to_image(state) # maybe edit image
		frames.append(image)

if __name__ == "__main__":
	main()