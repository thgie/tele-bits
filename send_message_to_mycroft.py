from mycroft_bus_client import MessageBusClient, Message

print('Setting up client to connect to a local mycroft instance')
client = MessageBusClient()
client.run_in_thread()

print('The monkeys are listening...')
client.emit(Message('speak', data={'utterance': 'trying my best'}))
client.emit(Message('mycroft.mic.listen'))
