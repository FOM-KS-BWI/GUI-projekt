from tkinter import *
from tkinter import ttk

import paho.mqtt.client as mqtt


class MQTTChatGUI(Frame):
    def __init__(self, root, **kw):
        super().__init__(**kw)
        self.root = root

        frm = ttk.Frame(self.root, padding=10)
        frm.grid()
        ttk.Label(frm, text="Broker").grid(column=0, row=0, sticky="w")
        self.broker_entry = ttk.Entry(frm, text="Broker")
        self.broker_entry.grid(column=1, row=0, columnspan=3, sticky="ew")
        self.connect_button = ttk.Button(frm, text="Connect")
        self.connect_button.grid(column=4, row=0, sticky="e")
        self.main_text = Text(frm, height=20, width=50)
        self.main_text.grid(column=0, row=1, columnspan=5)
        ttk.Label(frm, text="Message").grid(column=0, row=2, sticky="w")
        self.message_entry = ttk.Entry(frm, text="Message")
        self.message_entry.grid(column=1, row=2, columnspan=3, sticky="we")
        self.message_entry.bind("<Return>", self.send_message)
        self.send_button = ttk.Button(frm, text="Send")
        self.send_button.grid(column=4, row=2, sticky="e")
        self.send_button.config(command=self.send_message)

        # set default values
        self.broker_entry.insert(0, "broker.mqttdashboard.com")

        # set callbacks
        # self.connect_button.config(command=connect_mqtt)
        # self.send_button.config(command=send_message)

        self.mqtt_client: mqtt.Client = mqtt.Client("Claudius")
        self.mqtt_client.connect("broker.mqttdashboard.com")
        self.mqtt_client.on_message = self.receive_message
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.loop_start()

    def receive_message(self, client, user_data, message):
        text = message.payload.decode("utf8")
        self.main_text.insert(END, text + '\n')

    def on_connect(self, client, userdata, flags, rc):
        print("Connected.")
        self.mqtt_client.subscribe("/BWI20KS/Chat")

    def send_message(self, event=None):
        message = self.message_entry.get()
        self.mqtt_client.publish("/BWI20KS/Chat", message)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = Tk()
    main_gui = MQTTChatGUI(root)
    root.mainloop()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
