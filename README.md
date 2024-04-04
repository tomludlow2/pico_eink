# eInk Display for PICO

This outlines setup instructions and usage instructions

# Setup
- Plug in with button held down
- Copy the uf2 file
- It will reboot
- Open Thonny and connect to the board (not the chip) in bottom right
- Install the micropython-urllib.urequest by going into Thonny and then package manager
- Configure `WIFI_CONFIG.py` and copy across `network_manager.py` to the Pico

# recent_energy.py
- Loads in recent energy and demonstrates how to output this to the Pico eInk Display.
- Reloads every 60 seconds


# Common Positions
- For a + / i / letter adj to buttons a/b/c
```
	graphics.text("+", 288, 15)
    graphics.text("-", 288, 55)    
    graphics.text("w", 286, 100)
```