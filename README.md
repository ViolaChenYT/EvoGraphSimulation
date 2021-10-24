# Overall Design


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
- communication range: 20
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
