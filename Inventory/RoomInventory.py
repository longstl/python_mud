from Inventory import Inventory


class RoomInventory(Inventory):
	def __init__(self, inventoryJson, owner):
		import EventHandlers.RoomInventory
		
		Inventory.__init__(self, inventoryJson, owner)

		self.attributes['hidden_items']		= []
		self.attributes['permanent_items']	= []
		
		if inventoryJson != None:
			if inventoryJson.has_key('hidden_items'):
				for itemJson in inventoryJson['hidden_items']:
					item = self.createItem(itemJson)
			
					if item != None:
						self.attributes['hidden_items'].append(item)
						
			if inventoryJson.has_key('permanent_items'):
				for itemJson in inventoryJson['permanent_items']:
					item = self.createItem(itemJson)
			
					if item != None:
						self.attributes['permanent_items'].append(item)
		
		self.addEventHandler(EventHandlers.RoomInventory.ItemDroppedHandler())
		self.addEventHandler(EventHandlers.RoomInventory.ActorAttemptedItemGrabHandler())
		self.addEventHandler(EventHandlers.RoomInventory.ActorGrabbedItemHandler())
		self.addEventHandler(EventHandlers.RoomInventory.WasObservedHandler())
		
		
	def describe(self):
		retVal = ''
		
		if len(self.attributes['items']) > 0:
			retVal = 'You see:'
			
			for item in self.attributes['items']:
				retVal = '{} {} {},'.format(retVal, item.attributes['adjective'], item.attributes['name'])
				
			retVal = retVal[0:-1]
			
		return retVal