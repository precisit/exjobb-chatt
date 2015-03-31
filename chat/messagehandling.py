import pika
import sys
import router

from pika.adapters.tornado_connection import TornadoConnection

# messagehandling via pika

class PikaClient(object)
	def __init__(self,io_loop):
		# giving unique queue for each consumer
		# self.queue_name = "queue-%s" % (id(self),)
		# create a new instance passing the io_loop used to connect to RabbitMQ
		self.io_loop = io_loop

        self.connected = False
        self.connecting = False
        self.connection = None
        self.channel = None
 
        self.event_listeners = set([])

    def connect(self):
        if self.connecting:
            pika.log.info('PikaClient: Already connecting to RabbitMQ')
            return
 
        pika.log.info('PikaClient: Connecting to RabbitMQ')
        self.connecting = True
 
        cred = pika.PlainCredentials('guest', 'guest')
        param = pika.ConnectionParameters(
            host='localhost',
            port=5672,
            virtual_host='/',
            credentials=cred
        )
 
        self.connection = TornadoConnection(param,
            on_open_callback=self.on_connected)
        self.connection.add_on_close_callback(self.on_closed)
 
    def on_connected(self, connection):
        pika.log.info('PikaClient: connected to RabbitMQ on localhost: 5672')
        self.connected = True
        self.connection = connection
        self.connection.channel(self.on_channel_open)
 
    def on_channel_open(self, channel):
        pika.log.info('PikaClient: Channel open, Declaring exchange')
        self.channel = channel

        # declare exchanges
        channel.exchange_declare(
            exchange = 'tornado-chat', 
        	type = 'direct'
        )

        # declare queues
        print('PikaClient: Exchange Declared, Declaring Queue')

        # client queue
        channels.queue_declare(self.on_queue_declared_client, queue = clientQueue, exclusive = True, auto_delete = True)

        # server queue
        channels.queue_declare(self.on_queue_declared_server, queue = serverQueue, exclusive = True, auto_delete = True)

    def on_queue_declared_client(self,queue):
        self.clientQueue = result.method.queue
        # binding queue
        self.channel.queue_bind(
            exchange = 'tornado-chat',
            queue = self.clientQueue
        )

        # client queue should use callback, when receiving a message
        self.channel.basic_consume(
            self.on_message_client,
            queue = self.clientQueue,
            routing_key = client_routing_key
        )

    def on_queue_declared_server(self,queue):
        self.serverQueue = result.method.queue
        # binding queue
        self.channel.queue_bind(
            exchange = 'tornado-chat'
            queue = self.serverQueue
        )

        # server queue should use callback, when receiving a message
        self.channel.basic_consume(
            self.on_message_server,
            queue = self.serverQueue,
            routing_key = server_routing_key
        )

    # def on_exchange_declared(self,frame):
    # 	print('PikaClient: Exchange Declared, Declaring Queue')
    # 	self.channel.queue_declare(
    #        auto_delete = True,
    # 		queue = self.queue_name,
    # 		durable = False,
    # 		exclusive = True,
    # 		callback = self.on_queue_declared
    #    )

    # def on_queue_declared(self,frame):
    # 	print('PikaClient: Queue Declared, Binding Queue')
    # 	self.channel.queue_bind(
    #         exchange = 'tornado',
    # 		queue = self.queue_name,
    # 		routing_key = 'tornado.*',
    # 		callback = self.on_queue_bound
    #     )

    def on_queue_bound(self,frame):
    	print('PikaClient: Message receive, delivery tag #%i' % method.delivery_tag)
 
    def on_closed(self, connection):
        pika.log.info('PikaClient: rabbit connection closed')
        self.io_loop.stop()
 
 	# on messages from server or client
    def on_message(self, channel, method, header, body):
        pika.log.info('PikaClient: message received: %s' % body)
        self.notify_listeners(event_factory(body))
 
    def notify_listeners(self, event_obj):
        # here we assume the message the sourcing app
        # post to the message queue is in JSON format
        event_json = json.dumps(event_obj)
 
        for listener in self.event_listeners:
            listener.write_message(event_json)
            pika.log.info('PikaClient: notified %s' % repr(listener))
 
    def add_event_listener(self, listener):
        self.event_listeners.add(listener)
        pika.log.info('PikaClient: listener %s added' % repr(listener))
 
    def remove_event_listener(self, listener):
        try:
            self.event_listeners.remove(listener)
            pika.log.info('PikaClient: listener %s removed' % repr(listener))
        except KeyError:
            pass