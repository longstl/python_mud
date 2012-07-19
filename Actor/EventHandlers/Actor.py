import Engine.RoomEngine

class ActorAttemptedDropHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_drop'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] != '':
				event.attributes['data']['room'] = Engine.RoomEngine.getRoom(receiver.attributes['roomID'])
				receiver.emitEvent(event)
				
				
				
				
class ItemDroppedHandler:
	def __init__(self):
		self.attributes = {'signature': 'item_dropped'}

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']

		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorInitiatedItemGrabHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_initiated_item_grab'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			if event.attributes['data']['itemName'] != '':
				event.attributes['data']['room'] = Engine.RoomEngine.getRoom(receiver.attributes['roomID'])
				receiver.emitEvent(event)
				
				
				
				
				
class ActorGrabbedItemHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_grabbed_item'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorAttemptedItemEquipHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_equip'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']

		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorAttemptedItemRemovalHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_removal'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']

		if event.attributes['data']['actor'] == receiver:
			receiver.emitEvent(event)
			
			
			
			
class ActorMovedFromRoomEventHandler:
	def __init__(self):
		self.attributes = {'signature':'actor_moved_from_room'}

	def handleEvent(self, event):		
		receiver	= event.attributes['receiver']
		actor		= event.attributes['data']['actor']

		if actor == receiver:
			destination = Engine.RoomEngine.getRoom(event.attributes['data']['exit'].attributes['destination'])
			
			event.attributes['data']['room'].removeEventSubscriber(receiver)
			
			destination.addEventSubscriber(receiver)
			
			receiver.attributes['roomID'] = destination.attributes['roomID']
			