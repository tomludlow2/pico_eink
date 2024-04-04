#Micropython when used with Pimoroni micropython

#To Import modules:
from picographics import PicoGraphics, DISPLAY_INKY_PACK
#DISPLAY_INKY_PACK is specific to the pico eink series

display = PicoGraphics(display = DISPLAY_INKY_PACK)
#or
#display = PicoGraphics(display = DISPLAY_INKY_PACK, rotate=90,(180,270))

#Drawing:  as it's a 16 bit display
display.set_pen(0) #black
display.set_pen(15) #white  

#Backlight
display.set_backlight(0.5)

#Clipping
display.set_clip(x,y, w, h)
display.remove_clip()

#Clear Display
display.clear()
#Equivalent to:
w, h = display.get_bounds()
display.rectangle(0,0,w,h)


#Update
display.update()
#Might be:
galactic_unicorn.update(display)


#Change font
font = [bitmap6, bitmap8, bitmap14_outline]
font = [sans, gothic, cursive, serif_italic, serif]
#When using vector fonts (sans...) need to set thickness
display.set_thickness(n)
#n=number of pixels

display.set_font(font)

#Draw text
display.text(text, x, y, wordwrap, scale, angle, spacing)

#Example:
#display.set_font("bitmap8")
#display.text("Hello World", 0, 0, scale=2)

#Measure - can do this to check width
width = display.measure_text(text, scale, spacing, fixed_width)
