from Event.Event import Event
from Command import Command
import Engine.ActorEngine

class Who(Command):
	def __init__(self):
		Command.__init__(self)
		

	def execute(self, source, args):
		feedbackEvent									= Event()
		feedbackEvent.attributes['signature']			= 'received_feedback'
		feedbackEvent.attributes['data']['feedback']	= Engine.ActorEngine.getPlayerList()
		feedbackEvent.attributes['data']['actor']		= source

		Engine.ActorEngine.emitEvent(feedbackEvent)