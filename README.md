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


## draw_graph.py

This module provides a function for drawing custom bar graphs on a display using Micropython and the PicoGraphics library.

### Description:
Draws a custom bar graph on the display using provided data.

### Parameters:
- `graph_data`: A list of tuples containing x and y coordinates for each data point in the graph.
- `LABEL`: A string representing the label for the graph.
- `graphics`: An instance of the PicoGraphics object used for drawing on the display.

### Constants:
- `SCREEN_WIDTH`: Width of the display screen.
- `SCREEN_HEIGHT`: Height of the display screen.
- `CHART_WIDTH`: Width of the chart area.
- `CHART_HEIGHT`: Height of the chart area.
- `MARGIN_TOP`: Top margin of the chart.
- `MARGIN_LEFT`: Left margin of the chart.

### Usage Example:
```python
from picographics import PicoGraphics, DISPLAY_INKY_PACK

# Initialize PicoGraphics object
graphics = PicoGraphics(DISPLAY_INKY_PACK)

# Define graph data
graph_data = [(1, 10), (2, 20), (3, 30), (4, 25), (5, 35)]

# Define graph label
LABEL = "Custom Graph"

# Draw the graph
draw_custom_graph(graph_data, LABEL, graphics)
```
