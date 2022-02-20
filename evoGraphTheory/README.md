# Overall Design
In this simulation, I attempt to recreate the simulation done in [the science robotics paper](https://www.science.org/doi/10.1126/scirobotics.abf1416#pill-citations).

The simulation animation is done with the python package [PyGame](https://www.pygame.org/wiki/GettingStarted)

-	Packages used and versions:
	- pygame 2.0.0 (SDL 2.0.12, python 3.8.9)

- instruction on running simulation:
	- in terminal, run
		- `<python location> toy0.py`
		- for me, it was `/usr/bin/python3 toy0.py`
		- for you, it may simply be `python toy0.py` (check pygame and python versions, they can be annoying) 

## Parameters
### Agent

- number of agents - currently 20
- radius -10
- step size - 3
- states
	- `NOIDEA`
	- `POLLING`
	- `COMMITTED`

### Site

- number of sites - currently 1
- radius - 75

### Interactions
- communication range: 50
- reset to NOIDEA with probability `1 - self.quality`

## Assumptions made
- boundary conditions:
	- currently looping around (left & right margin connected)
- `direct switching` mode for conflict handling
	- committed robots will switch to `NOIDEA`
	- alternative: cross-inhibition, switch to polling state


## Questions and Clarifications
- random movements seem really ineffective now.
	- potential solution: set direction every $m$ time steps, and make a movement of random distance every time step / make a movement within a range of the general direction picked every time step

## Future work
- try more than 1 site with varying quality
