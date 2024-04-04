#Test download data from pico_display endpoint
import WIFI_CONFIG
import time
import uasyncio
import ujson
from network_manager import NetworkManager
from urllib import urequest
from picographics import PicoGraphics, DISPLAY_INKY_PACK

ENDPOINT= "http://192.168.68.78:52526/pico_display"
MONTHNAMES = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
graphics = PicoGraphics(DISPLAY_INKY_PACK)
last_date = ""
WIDTH, HEIGHT = graphics.get_bounds()



def status_handler(mode, status, ip):
    graphics.set_update_speed(2)
    graphics.set_pen(15)
    graphics.clear()
    graphics.set_pen(0)
    graphics.text("Network: {}".format(WIFI_CONFIG.SSID), 10, 10, scale=2)
    status_text = "Connecting..."
    if status is not None:
        if status:
            status_text = "Connection successful!"
        else:
            status_text = "Connection failed!"

    graphics.text(status_text, 10, 30, scale=2)
    graphics.text("IP: {}".format(ip), 10, 60, scale=2)
    graphics.update()

network_manager = NetworkManager(WIFI_CONFIG.COUNTRY, status_handler=status_handler)

while True:
    graphics.set_font("bitmap8")
    graphics.set_update_speed(1)

    uasyncio.get_event_loop().run_until_complete(network_manager.client(WIFI_CONFIG.SSID, WIFI_CONFIG.PSK))

    date = list(time.localtime())[:3]
    date.append(MONTHNAMES[date[1] - 1])

    if "{3} {2}, {0}".format(*date) == last_date:
        time.sleep(60)
        continue

    url = ENDPOINT 
    print("Requesting URL: {}".format(url))
    j = ujson.load(urequest.urlopen(url))
    print(j['output'][0])
    
    #Extract the most recent data point
    latest_data = j["output"][-2]
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
    
    graphics.update()
    

    time.sleep(60)
