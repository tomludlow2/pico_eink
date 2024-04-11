def draw_custom_graph(graph_data, LABEL, graphics):
    # Extract x and y coordinates from graph_data
    x_coords, y_coords = zip(*graph_data)
    
    # Constants for chart dimensions and margins
    SCREEN_WIDTH = 296
    SCREEN_HEIGHT = 128
    CHART_WIDTH = 220
    CHART_HEIGHT = 80
    MARGIN_TOP = 28
    MARGIN_LEFT = 50
    
    # Clear the screen
    graphics.set_pen(15)
    graphics.clear()
    
    # Calculate maximum y-coordinate for scaling
    max_y = max(y_coords)
    
    bar_width = CHART_WIDTH // len(x_coords)
    
    # Set pen color for the bars (black)
    graphics.set_pen(0)
    for i, y_coord in enumerate(y_coords):
        bar_height = int((y_coord / max_y) * CHART_HEIGHT)
        bar_x = MARGIN_LEFT + i * bar_width
        bar_y = MARGIN_TOP + CHART_HEIGHT - bar_height
        graphics.rectangle(bar_x, bar_y, bar_width - 1, bar_height)
    
    # Set pen color for the axes (black)
    graphics.line(MARGIN_LEFT - 5, MARGIN_TOP, MARGIN_LEFT - 5, MARGIN_TOP + CHART_HEIGHT)
    graphics.line(MARGIN_LEFT, MARGIN_TOP + CHART_HEIGHT, MARGIN_LEFT + CHART_WIDTH, MARGIN_TOP + CHART_HEIGHT)
    
    # Draw the date labels
    graphics.set_font("bitmap8")
    for i, x_coord in enumerate(x_coords):
        label_x = int(MARGIN_LEFT + (i + 0.5) * bar_width - 5)
        label_y = int(MARGIN_TOP + CHART_HEIGHT + 5)
        graphics.text(str(x_coord), label_x, label_y, 2)
    
    # Draw the y-axis labels
    graphics.text("0", MARGIN_LEFT - 26, MARGIN_TOP + CHART_HEIGHT + 2, 2)  # Label for 0%
    graphics.text("{:.1f}".format(max_y / 2), MARGIN_LEFT - 46, MARGIN_TOP + CHART_HEIGHT // 2 + 2, 2)  # Label for 50%
    graphics.text("{:.1f}".format(max_y), MARGIN_LEFT - 46, MARGIN_TOP, 2)  # Label for 100%
    
    # Draw the label at the top left
    graphics.text(LABEL, 2, 2, 2)
    
    graphics.update()
