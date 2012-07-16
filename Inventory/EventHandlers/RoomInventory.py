import re
from Event.Event import Event


pattern = re.compile('[1-9][0-9]*')


class ItemDroppedHandler:
	def __init__(self):
		self.attributes = {'signature': 'item_dropped'}

	def handleEvent(self, event):		
		receiver = event.attributes['receiver']
		
		receiver.attributes['items'].append(event.attributes['data']['item'])
		
		
		
		
class ActorAttemptedItemGrabHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_attempted_item_grab'}

	def handleEvent(self, event):
		receiver	= event.attributes['receiver']
		target		= event.attributes['data']['itemName']
		targetList	= filter(lambda item : 
								item.attributes['name'].lower().startswith(target.lower()), 
							receiver.attributes['items'])

		if len(targetList) == 0:
			feedbackEvent									= Event()
			feedbackEvent.attributes['signature']			= 'received_feedback'
			feedbackEvent.attributes['data']['feedback']	= 'You don\'t see that.'
			feedbackEvent.attributes['data']['actor']		= event.attributes['data']['actor']

			event.attributes['data']['room'].emitEvent(feedbackEvent)
		else:
			event.attributes['data']['item']	= targetList[0]
			args								= event.attributes['data']['args']
					
			if len(args) >= 1 and args[0] != '':
				if pattern.match(args[0]) and re.search('[^0-9]', args[0]) == None:
					itemNumber = int(args[0]) - 1
					
					if itemNumber < len(targetList):
						event.attributes['data']['item'] = targetList[itemNumber]
			
			receiver.emitEvent(event)
			
			
			
			
class ActorGrabbedItemHandler:
	def __init__(self):
		self.attributes = {'signature': 'actor_grabbed_item'}

	def handleEvent(self, event):
		receiver = event.attributes['receiver']
		
		receiver.attributes['items'].remove(event.attributes['data']['item'])

		receiver.emitEvent(event)