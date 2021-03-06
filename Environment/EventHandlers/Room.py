from Event.Event import Event
from Event.EventHandler import EventHandler
import Engine.RoomEngine
import Engine.AffectEngine
from lib import ANSI
import re
from Actor.Player import Player


pattern	= re.compile('[1-9][0-9]*')


class ActorAttemptedMovementEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_attempted_movement'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['room'] == receiver:
			actor		= event.attributes['data']['source']
			direction	= event.attributes['data']['direction']
		
			if direction != None:
				movedFromEvent								= Event()
				movedFromEvent.attributes['signature']		= 'actor_moved_from_room'
				movedFromEvent.attributes['data']['actor']	= actor
				movedFromEvent.attributes['data']['exit']	= direction
				movedFromEvent.attributes['data']['room']	= receiver
			
				movedToEvent								= Event()
				movedToEvent.attributes['signature']		= 'actor_added_to_room'
				movedToEvent.attributes['data']['actor']	= actor
				movedToEvent.attributes['data']['room']		= Engine.RoomEngine.getRoom(direction.attributes['destination'])
				
				Engine.RoomEngine.emitEvent(movedFromEvent)
				Engine.RoomEngine.emitEvent(movedToEvent)




class ActorMovedFromRoomEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_moved_from_room'

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['room'] == receiver:
			actor = event.attributes['data']['actor']
			
			if isinstance(actor, Player):
				receiver.removePlayer(actor)
			else:
				receiver.removeNPC(actor)
				
			receiver.emitEvent(event)
			



class ActorAddedToRoomEventHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_added_to_room'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
	
		if event.attributes['data']['room'] == receiver:
			actor = event.attributes['data']['actor']
			
			if isinstance(actor, Player):
				receiver.addPlayer(actor)
			else:
				receiver.addNPC(actor)
			
			receiver.emitEvent(event)
			
			
			
			
			
class ActorEmotedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_emoted'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']

		if event.attributes['data']['room'] == receiver:
			targetName	= event.attributes['data']['target']
			target		= None
			actorList	= filter(lambda actor: 
									actor != event.attributes['data']['emoter'],
								receiver.attributes['players'] + receiver.attributes['npcs'])

			if targetName != None and targetName != '':
				targetList	= filter(lambda actor : 
										actor.attributes['name'].lower().startswith(targetName.lower()),
									 actorList)

				if len(targetList) > 0:
					target = targetList[0]
				else:
					emoter											= event.attributes['data']['emoter']
					feedbackEvent									= Event()
					feedbackEvent.attributes['signature']			= 'received_feedback'
					feedbackEvent.attributes['data']['feedback']	= 'You don\'t see that here.'
					feedbackEvent.attributes['data']['actor']		= emoter

					receiver.emitEvent(feedbackEvent)

					return

			event.attributes['data']['target'] = target	

			receiver.emitEvent(event)




class ActorObservedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='actor_observed'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['room'] == receiver:
			observer	= event.attributes['data']['observer']
			target		= event.attributes['data']['target']
			players		= receiver.attributes['players']
			npcs		= receiver.attributes['npcs']
			inventory	= receiver.attributes['inventory']
			items		= inventory.attributes['items']
			permItems	= inventory.attributes['permanent_items']
			hiddenItems = inventory.attributes['hidden_items']
			mergedList	= players + npcs + items + permItems + hiddenItems
			
			if target in set(mergedList):
				lookEvent									= Event()
				lookEvent.attributes['data']['observer']	= observer
				lookEvent.attributes['data']['target']		= target
				lookEvent.attributes['signature']			= 'was_observed'

				receiver.emitEvent(lookEvent)
			else:
				feedbackEvent									= Event()
				feedbackEvent.attributes['signature']			= 'received_feedback'
				feedbackEvent.attributes['data']['feedback']	= 'You don\'t see that here.'
				feedbackEvent.attributes['data']['actor']		= observer

				receiver.emitEvent(feedbackEvent)
				




class WasObservedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='was_observed'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['room'] == receiver:		
			player		= event.attributes['data']['observer']
			description = [ANSI.red(receiver.attributes['name']) + '\n\r']
			exitList	= 'Obvious exits:'
			playerList	= filter(lambda p: p != player, receiver.attributes['players'])
			npcList		= receiver.attributes['npcs']

			for line in receiver.attributes['description']:
				description.append(line)

			for exit in receiver.attributes['exits']:
				if exit.attributes['isHidden'] == False:
					exitList = exitList + ' ' + exit.attributes['name'] + ','

			if exitList == 'Obvious exits:':
				exitList = 'Obvious exits: none'

			if exitList.endswith(','):
				exitList = exitList[0:-1]

			description.append(ANSI.blue(exitList))
			
			if len(playerList) > 0:
				playerLine = 'Players:'

				for p in playerList:
					playerLine = playerLine + ' ' + p.attributes['name'] + ','

				if playerLine.endswith(','):
					playerLine = playerLine[0:-1]

				description.append(ANSI.green(playerLine))
			
			if len(npcList) > 0:
				npcLine		= 'NPCs:'
				listedNPCs	= []

				for npc in npcList:
					npcName = npc.attributes['name']
					
					if npcName not in set(listedNPCs):
						listedNPCs.append(npcName)
						
						reducedList = filter(lambda element: 
												element.attributes['name'] == npcName,
											 npcList)
						adjective	= npc.attributes['adjective']
					
						if len(reducedList) > 1:
							adjective	= '{}'.format(len(reducedList))
							npcName		= npc.attributes['pluralName']
						
						if len(adjective) > 0:
							npcLine = '{} {} {},'.format(npcLine, adjective, npcName)
						else:
							npcLine = '{} {}'.format(npcLine, npcName)

				if npcLine.endswith(','):
					npcLine = npcLine[0:-1]

				description.append(npcLine)
			
			inventory	= receiver.attributes['inventory']
			itemList	= inventory.describe()
			
			if itemList != '':
				description.append(itemList)

			describeEvent									= Event()
			describeEvent.attributes['signature']			= 'entity_described_self'
			describeEvent.attributes['data']['description'] = description
			describeEvent.attributes['data']['observer']	= player

			receiver.emitEvent(describeEvent)

		
		

class PlayerLogoutHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='player_logout'
		
	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		receiver.removePlayer(event.attributes['data']['actor'])




class SpellCastAttempted(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] ='spell_cast_attempted'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']

		if event.attributes['data']['room'] == receiver:			
			source		= event.attributes['data']['source']
			targetName	= event.attributes['data']['target']
			spell		= event.attributes['data']['spell']
			target		= None
			
			if targetName == None:
				target = source
			else:
				targetList	= filter(lambda actor : 
										actor.attributes['name'].lower().startswith(targetName.lower()), 
									receiver.attributes['players'] + receiver.attributes['npcs'])

				if len(targetList) == 0:
					feedbackEvent									= Event()
					feedbackEvent.attributes['signature']			= 'received_feedback'
					feedbackEvent.attributes['data']['feedback']	= 'You don\'t see that here.'
					feedbackEvent.attributes['data']['actor']		= source

					receiver.emitEvent(feedbackEvent)
				else:
					target = targetList[0]
			
			Engine.AffectEngine.executeAffect(spell, source, target)
			
			
			

class ItemDroppedHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'item_dropped'

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['room'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorAttemptedItemGrabHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_attempted_item_grab'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']

		if event.attributes['data']['room'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorGrabbedItemHandler(EventHandler):
	def __init__(self, adjusters):
		EventHandler.__init__(self, adjusters)
		self.attributes['signature'] = 'actor_grabbed_item'

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['room'] == receiver:
			receiver.emitEvent(event)