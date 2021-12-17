from tkinter import *
from tkinter import ttk
import random
import string

# Import the MQTT-lib
import paho.mqtt.client as mqtt

class MQTTChatGUI(Frame):
    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.root = root
        self.root.title("MQTT-Chat")

        frm = ttk.Frame(self.root, padding=10)
        frm.grid()
        ttk.Label(frm, text="Nickname").grid(column=0, row=0, sticky="w")
        # create field for broker enrty
        self.broker_entry = ttk.Entry(frm, text="Nickname")
        self.broker_entry.grid(column=1, row=0, columnspan=3, sticky="ew")
        # Create text field
        self.main_text = Text(frm, height=20, width=50)
        self.main_text.grid(column=0, row=1, columnspan=5)
        ttk.Label(frm, text="Message").grid(column=0, row=2, sticky="w")
        # Create field for message
        self.message_entry = ttk.Entry(frm, text="Message")
        self.message_entry.grid(column=1, row=2, columnspan=3, sticky="we")
        self.message_entry.bind("<Return>", self.send_message)
        # Create send-button
        self.send_button = ttk.Button(frm, text="Send")
        self.send_button.grid(column=4, row=2, sticky="e")
        self.send_button.config(command=self.send_message)
        self.scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.main_text.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        self.main_text.config(yscrollcommand=self.scrollbar.set)


        # set default values
        self.broker_entry.insert(0, "Nickname")

        # set callbacks
        # self.connect_button.config(command=connect_mqtt)
        # self.send_button.config(command=send_message)

        letters = string.ascii_lowercase
        self.id = ''.join(random.choice(letters) for i in range(20))
        self.mqtt_client: mqtt.Client = mqtt.Client(self.id)
        self.mqtt_client.connect("broker.mqttdashboard.com")
        self.mqtt_client.on_message = self.receive_message
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.loop_start()

    def receive_message(self, client, user_data, message):
        """
        nimmt Nachricht entgegen
        :param client:
        :param user_data:
        :param message: Message
        :return:
        """
        text = message.payload.decode("utf8")
        self.main_text.insert(END, text + '\n')

    def on_connect(self, client, userdata, flags, rc):
        """
        Verbindet sich mit dem Topic und schreibt einmalig 'connected'
        :param client:
        :param userdata:
        :param flags:
        :param rc:
        :return:
        """
        # Print "connected" after reconnect
        print("Connected.")
        # Get messages from Chat, QoS1
        self.mqtt_client.subscribe("/BWI20KS/Chat", 1)

    def send_message(self, event=None):
        message = self.message_entry.get()
        # Delete entry in message field after sending
        self.message_entry.delete(0, END)
        # publish message after send, QoS1
        self.mqtt_client.publish("/BWI20KS/Chat", message, 1)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    main_gui = MQTTChatGUI(root)
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
