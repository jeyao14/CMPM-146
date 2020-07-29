

def if_neutral_planet_available(state):
    return any(state.neutral_planets())


def have_largest_fleet(state):
    return sum(planet.num_ships for planet in state.my_planets()) \
             + sum(fleet.num_ships for fleet in state.my_fleets()) \
           > sum(planet.num_ships for planet in state.enemy_planets()) \
             + sum(fleet.num_ships for fleet in state.enemy_fleets())

def have_more_planets(state):
	return len(state.my_planets()) > len(state.enemy_planets())

def have_largest_growth(state):
	return sum(planet.growth_rate for planet in state.my_planet()) \
             > sum(planet.growth_rate for planet in state.enemy_planets())

def need_growth(state):
	for planet in state.my_planets():
		if planet.growth_rate < 7:
			return True
	return False

