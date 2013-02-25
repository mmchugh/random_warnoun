from .models import Player, Caster, RoundPairing
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.db.models import Max
from django.core.urlresolvers import reverse

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
				previous = RoundPairing.objects.get(player=player, caster=caster)
			except RoundPairing.DoesNotExist: # this player/caster pairing works
				pairing = RoundPairing()
				pairing.player = player
				pairing.caster = caster
				pairing.round_number = round_number
				pairing.save()

				caster_pool.remove(caster)	# prevent multiple caster pairings
				break

def index(request):
	rounds = RoundPairing.objects.order_by('round_number')
	current_rounds = RoundPairing.current_rounds()
	return render(request, 'index.html', 
		{'rounds': rounds, 
		 'current_rounds': current_rounds, }, )

def view_players(request):
	players = Player.objects.all()

	return render(request, 'selections/players.html', 
		{'players': players}, )

def view_casters(request):
	casters = Caster.objects.all()

	return render(request, 'selections/casters.html', 
		{'casters': casters}, )

def create_tournament(request):
	rounds = request.GET.get('rounds', None)
	if not rounds:
		return HttpResponse('You must set the number of rounds!')

	# first, delete all current round pairings
	RoundPairing.objects.all().delete()
	
	for round_number in range(int(rounds)):
		_generate_round(round_number + 1)

	return redirect(reverse('view-rounds'))

def add_tournament_round(request):
	# grab the highest round number in pairings and treat as the round count
	current_rounds = RoundPairing.current_rounds()

	_generate_round(current_rounds + 1)

	return redirect(reverse('view-rounds'))

def tournament_rounds(request):
	players = Player.objects.order_by('name')
	rounds = RoundPairing.current_rounds()
	return render(request, 'selections/tournament_rounds.html', 
		{'players': players,
		 'rounds': range(rounds), }, )

def printable_round(request, round_number):
	pairings = RoundPairing.objects.filter(round_number=round_number).order_by('player__name')

	return render(request, 'selections/printable_round.html', 
		{'pairings': pairings}, )