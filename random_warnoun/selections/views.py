from .models import Player, Caster, RoundPairing
from django.http import HttpResponse

import random

def _generate_round(round_number):
	"""
	Generate a new round of the given round number.

	No two players will be assigned the same caster in a single round.
	No player will be assigned a caster they were previously assigned.
	"""

	caster_pool = list(Caster.objects.all())
	# a naive loop for assigning casters to players. As long as the number of
	# casters in the pool is > players + total rounds, this is guaranteed to
	# eventually finish. The larger the pool, the less likely collisions will
	# slow down the random picking

	for player in Player.objects.all():
		while True:
			caster = random.choice(caster_pool)
			try:
				previous = RoundPairing.objects.get(player=player, 
													caster=caster, 
													round_number__lt=round_number)
			except RoundPairing.DoesNotExist:	# this player/caster pairing works
				pairing = RoundPairing()
				pairing.player = player
				pairing.caster = caster
				pairing.round_number = round_number
				pairing.save()

				caster_pool.remove(caster)	# prevent multiple caster pairings
				break

def create_tournament(request):
	rounds = request.GET.get('rounds', None)
	if not rounds:
		return HttpResponse('You must set the number of rounds!')

	for round_number in range(int(rounds)):
		_generate_round(round_number + 1)

