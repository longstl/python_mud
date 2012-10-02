from Event.Event import Event
from Command import Command
import Engine.RoomEngine

class Look(Command):
	def __init__(self):
		Command.__init__(self)


	def execute(self, source, args):
		actor		= source
		roomID		= actor.attributes['roomID']
		room		= Engine.RoomEngine.getRoom(roomID)
		lookEvent	= Event()
	
		lookEvent.attributes['signature']			= 'actor_observed'
		lookEvent.attributes['data']['observer']	= actor
		lookEvent.attributes['data']['room']		= room
	
		if args == None or len(args) == 0:
			lookEvent.attributes['data']['target']	= None
		else:				
			lookEvent.attributes['data']['target']	= args[0]
		
		actor.emitEvent(lookEvent)