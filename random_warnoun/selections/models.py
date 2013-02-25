from django.db import models

FACTIONS = (
	(1, 'Cryx'),
	(2, 'Cygnar'),
	(3, 'Khador'),
	(4, 'Menoth'),
	(5, 'Retribution'),
	(6, 'Mercenaries'),
	(7, 'Circle'),
	(8, 'Legion'),
	(9, 'Skorne'),
	(10, 'Trollbloods'),
	(11, 'Minions'),
	)

class Caster(models.Model):
	name = models.CharField(max_length=75)
	faction = models.IntegerField(choices=FACTIONS)

	def __unicode__(self):
		return self.name

class Player(models.Model):
	name = models.CharField(max_length=50)
	faction = models.IntegerField(choices=FACTIONS)

	def __unicode__(self):
		return self.name

	def caster_pairings(self):
		pairings = RoundPairing.objects.filter(player=self).order_by('round_number')
		return [pairing.caster for pairing in pairings]

class RoundPairing(models.Model):
	player = models.ForeignKey(Player)
	caster = models.ForeignKey(Caster)
	round_number = models.PositiveIntegerField()

	def __unicode__(self):
		return '%s: %s (round %d)' % (self.player, self.caster, self.round_number)

	@staticmethod
	def current_rounds():
		rounds = RoundPairing.objects.all().aggregate(models.Max('round_number'))['round_number__max']
		return rounds if rounds else 0