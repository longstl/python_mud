from Event.Event import Event
from Event.EventHandler import EventHandler
from Engine import Engine
import CommandEngine
import ActorEngine
from Environment.Room import Room
from Environment.Exit import Exit
import Driver.ConnectionListUpdater
import os
import json


def addEventSubscriber(subscriber):
	RoomEngine.instance.addEventSubscriber(subscriber)
	

def emitEvent(event, emitter):
	#print 'RoomEngine received event {} from {}'.format(event.attributes['signature'], emitter)
	RoomEngine.instance.emitEvent(event)


def getRoom(roomID):
	return RoomEngine.instance.getRoom(roomID)


class RoomEngine(Engine):
	instance = None
	
	def __init__(self):
		Engine.__init__(self)
		
		attributes = {
			'roomMap'	: {},
			'roomList'	: []
		}
		
		for key in attributes.keys():
			self.attributes[key] = attributes[key]
		
		self.addEventHandler(PlayerLoginEventHandler())
		self.addEventHandler(RoomEnginePlayerLogoutEventHandler())
		
		RoomEngine.instance = self
		
		self.buildWorld()
		
		Driver.ConnectionListUpdater.addEventSubscriber(self)
		CommandEngine.addEventSubscriber(self)
		
	
	def buildWorld(self):
		currentDir	= os.getcwd()
		worldDir	= currentDir + '/Content/world' 
		fileList	= os.listdir(worldDir)
		
		for fname in fileList:			
			if fname.endswith('.txt'):
				filePath	= '{}/{}'.format(worldDir, fname)
				roomFile	= open(filePath, 'r')
				jsonString	= roomFile.read()
				jsonObj		= json.loads(jsonString)
				room		= Room()
				
				roomFile.close()
				
				for key in jsonObj.keys():
					if key == 'exits':
						for exitJson in jsonObj[key]:
							exit = Exit()
							for field in exitJson.keys():
								exit.attributes[field] = exitJson[field]
							
							room.attributes[key].append(exit)
					else:
						room.attributes[key] = jsonObj[key]

				self.attributes['roomList'].append(room)
				self.attributes['roomMap'][room.attributes['roomID']] = room

	
	
	def getRoom(self, roomID):
		return self.attributes['roomMap'][roomID]




class PlayerLoginEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)

		self.attributes['signature']	= 'player_login'
		self.attributes['function']		= self.playerLogin


	def playerLogin(self, receiver, event):
		player			= event.attributes['data']['player']
		roomID			= player.attributes['roomID']
		room			= receiver.getRoom(roomID)
		playerInEvent	= Event()

		playerInEvent.attributes['signature']		= 'actor_added_to_room'
		playerInEvent.attributes['data']['actor']	= player
		playerInEvent.attributes['data']['room']	= room

		receiver.emitEvent(playerInEvent)




class RoomEnginePlayerLogoutEventHandler(EventHandler):
	def __init__(self):
		EventHandler.__init__(self)

		self.attributes['signature']	= 'player_logout'
		self.attributes['function']		= self.playerLogout


	def playerLogout(self, receiver, event):
		connection	= event.attributes['data']['connection']
		player		= connection.attributes['player']
		roomID		= player.attributes['roomID']
		room		= receiver.getRoom(roomID)
		logoutEvent = Event()

		logoutEvent.attributes['signature']				= 'player_logout'
		logoutEvent.attributes['data']['actor']			= player
		logoutEvent.attributes['data']['exitMessage']	= None

		receiver.emitEvent(logoutEvent)