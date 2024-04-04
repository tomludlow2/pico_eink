#Test download data from pico_display endpoint
import WIFI_CONFIG
import time
import uasyncio
import ujson
from network_manager import NetworkManager
from urllib import urequest
from picographics import PicoGraphics, DISPLAY_INKY_PACK
from pimoroni import Button

ENDPOINT= "http://192.168.68.78:52526/pico_display"
MONTHNAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
graphics = PicoGraphics(DISPLAY_INKY_PACK)
last_date = ""
WIDTH, HEIGHT = graphics.get_bounds()

index = -2

button_a = Button(12)
button_b = Button(13)
button_c = Button(14)

energy_data = []
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


def update_screen(index):
    graphics.set_font("bitmap8")
    graphics.set_update_speed(1)
    #Extract the most recent data point
    latest_data = energy_data[index]
    date = latest_data["date"]
    a = float(latest_data["electric_cost"])
    b = float(latest_data["gas_cost"])
    total_cost =  a + b
    total_cost_disp = "£{:.2f}".format(total_cost)
    
    
    #Do some display stuff!
    x_offset = 160
    y_offset = 10
    line_spacing = 20

    graphics.set_pen(15)
    graphics.clear()
    graphics.set_pen(0)
    
    graphics.text("Usage for " + date, 40, y_offset)
    y_offset += line_spacing
    graphics.text("Electric Cost: ", 0, y_offset)
    graphics.text("£" + latest_data["electric_cost"], x_offset, y_offset)
    

    y_offset += line_spacing
    graphics.text("Electric Usage: ", 0, y_offset)
    graphics.text(latest_data["electric_usage"] + "kWh", x_offset, y_offset)
    

    y_offset += line_spacing
    graphics.text("Gas Cost: ", 0, y_offset)
    graphics.text("£" + latest_data["gas_cost"], x_offset, y_offset)
    
    y_offset += line_spacing
    graphics.text("Gas Usage: ", 0, y_offset)
    graphics.text(latest_data["gas_usage"] + "kWh", x_offset, y_offset)
    
    y_offset += line_spacing
    graphics.text("TOTAL COST ", 0, y_offset)
    graphics.text(total_cost_disp, x_offset+20, y_offset)
    
    graphics.text("+", 288, 15)
    graphics.text("-", 288, 55)    
    graphics.text("c", 286, 100)
    
    graphics.update()
    
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
    

update_data()
current_index = -4
#update_screen(current_index)
#home_screen()



while True:
    if button_a.read():
        current_index = current_index +1
        if( current_index == -1 ):
            current_index = (len(energy_data)*-1)
        print("Button A Pressed", "New Index:", current_index)
        update_screen(current_index)
    elif button_b.read():
        current_index = current_index -1
        if( current_index == (len(energy_data)*-1)-1 ):
            current_index = -2            
        print("Button B Pressed", "New Index:", current_index)
        update_screen(current_index)
    elif button_c.read():
        print("Button C Pressed")
        connection_screen(status_connection, current_ip, last_data_point)
    time.sleep(0.1)

    
        
    
