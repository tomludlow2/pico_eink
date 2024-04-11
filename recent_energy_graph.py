#Test download data from pico_display endpoint
import WIFI_CONFIG
import time
import uasyncio
import ujson
from network_manager import NetworkManager
from urllib import urequest
from picographics import PicoGraphics, DISPLAY_INKY_PACK
from pimoroni import Button
from draw_graph import draw_custom_graph

ENDPOINT= "https://energy.465streetlane.co.uk/pico_display"
MONTHNAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
graphics = PicoGraphics(DISPLAY_INKY_PACK)
last_date = ""
WIDTH, HEIGHT = graphics.get_bounds()

index = -2

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

data_file = "sample_data.json"
energy_data =[]
sample_energy_data = []
with open('sample_data.json', 'r') as file:
    data = ujson.load(file)
    sample_energy_data = data["sample_data"]
    sample_energy_data.pop()
    print("Sample Data Loaded")
    print(sample_energy_data)

status_connection = "Disconnected"
last_data_point = "none"
current_ip = ""


def status_handler(mode, status, ip):
    global current_ip
    current_ip = ip    
    connection_screen("Connecting", (ip), "Please Wait")
    if status is not None:
        global status_connection
        if status:            
            status_text = "Connection successful!"
            status_connection = "Connected"
            global last_data_point
            connection_screen("Connected", (ip), last_data_point)
        else:
            status_text = "Connection failed!"
            status_connection = "Failed"
            connection_screen("Failed", (ip), "Error")

   

network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)

def update_data():
    graphics.set_font("bitmap8")
    graphics.set_update_speed(1)
    while True:
        uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))

        date = list(time.localtime())[:3]
        date.append(MONTHNAMES[date[1] - 1])

        if "{3} {2}, {0}".format(*date) == last_date:
            time.sleep(60)
            continue

        url = ENDPOINT 
        print("Requesting URL: {}".format(url))
        j = ujson.load(urequest.urlopen(url))
        print("Loaded")
        
        global energy_data
        energy_data = j["output"]
        print(energy_data)
        global last_data_point
        last_data_point = energy_data[-1]["date"]
        return

def connection_screen(connected, ip, last_date):
    global status_connection
    graphics.set_font("bitmap8")
    graphics.set_update_speed(1)
    graphics.set_pen(15)
    graphics.clear()
    graphics.set_pen(0)
    
    
    graphics.rectangle(5, 5, 82, 24)
    graphics.text(" Energy Monitor", 88, 10)
    graphics.line(94, 28, 230, 28,2)
    
    graphics.text("Connection:", 20, 36)
    graphics.text("IP:", 20, 64)
    graphics.rectangle(140,60,128,22)
    
    graphics.text("Last Data:",20, 92)
    graphics.rectangle(140, 88, 128, 22)
    
    
    graphics.set_pen(15)
    graphics.text("RPi Pico", 10, 10)
    graphics.text(ip, 150, 64)
    
    if( connected == "Connected"):
        graphics.set_pen(0)
        graphics.rectangle(140,32,60,22)
        graphics.set_pen(15)
        graphics.text("LIVE", 150,36)
    elif( connected == "Connecting"):
        graphics.set_pen(0)
        graphics.rectangle(140,32,60,22)
        graphics.set_pen(15)
        graphics.text("CONN", 150,36)
    elif( connected == "Failed"):
        graphics.set_pen(0)
        graphics.rectangle(140,32,60,22)
        graphics.set_pen(15)
        graphics.text("FAIL", 150,36)
        
    if( last_date is not None ):
        graphics.set_pen(15)
        graphics.text(last_date, 150, 92)
    #graphics.text("RPi Pico Energy Connection", 0, 0)
    #graphics.text("Data connection: " + status_connection, 0, 40)
    graphics.update()



def graph_electric_usage():
    print("Drawing Electric Usage")
    # Extract electric usage data and day from sample_energy_data
    electric_usage_data = [float(entry['electric_usage']) for entry in sample_energy_data]
    days = [entry['date'].split('-')[0] for entry in sample_energy_data]
    
    # Call draw_custom_graph function with extracted data
    draw_custom_graph(zip(days, electric_usage_data), "ElectricUsg", graphics)

    print("Done")
    
def graph_gas_usage():
    print("Drawing Gas Usage")
    # Extract electric usage data and day from sample_energy_data
    electric_usage_data = [float(entry['gas_usage']) for entry in sample_energy_data]
    days = [entry['date'].split('-')[0] for entry in sample_energy_data]
    
    # Call draw_custom_graph function with extracted data
    draw_custom_graph(zip(days, electric_usage_data), "GasUsg", graphics)
    print("Done")

update_data()


while True:
    if button_a.read():
        graph_gas_usage()
    elif button_b.read():
        graph_electric_usage()
    elif button_c.read():
        print("Button C Pressed")
        connection_screen(status_connection, current_ip, last_data_point)
    time.sleep(0.1)

    
        
    
