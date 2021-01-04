import GauntletObjects

gauntlet_objects = GauntletObjects.GauntletEntities(0)

gauntlet_objects.generate_random_event(10, 1, 10, 1)

print(gauntlet_objects.__dict__)