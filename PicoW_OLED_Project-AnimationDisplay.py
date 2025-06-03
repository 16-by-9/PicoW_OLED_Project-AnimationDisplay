import board
import busio
import time
import math
import adafruit_ssd1306

# ──────────────────────────────────────────────────────────────────────────────
# SETTINGS (match the Arduino/ESP32 sketch)
# ──────────────────────────────────────────────────────────────────────────────
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# Center of the atom
center_x = SCREEN_WIDTH // 2   # 64
center_y = SCREEN_HEIGHT // 2  # 32

# Nucleus (three nucleons) configuration
nucleus_radius = 4   # radius of each proton/neutron dot
offset = 5           # offset between nucleus dots

# Electron orbit configuration
orbit_radius = 26     # how far the electron orbits from center
electron_radius = 2   # radius of the electron dot

# Animation timing (≈30 FPS)
total_frames = 20
angle_increment = 360.0 / total_frames  # degrees per frame
frame_delay = 0.001  # seconds (≈1 ms)
# ──────────────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────────────
# UTILITY FUNCTIONS FOR DRAWING CIRCLES ON THE FRAMEBUFFER
# (MicroPython/CircuitPython’s framebuf does not include a built-in circle method,
# so we implement our own for outline circles and filled circles.)
# ──────────────────────────────────────────────────────────────────────────────

def draw_circle_outline(fbuf, x0: int, y0: int, r: int, color: int):
    """
    Draw an unfilled (outline) circle using Bresenham’s algorithm.
    fbuf: the SSD1306 display object (framebuffer)
    (x0, y0): center
    r: radius
    color: 1 = white, 0 = black
    """
    x = r
    y = 0
    err = 1 - r

    while x >= y:
        # Plot the eight symmetric points around the circle
        fbuf.pixel( x0 + x, y0 + y, color)
        fbuf.pixel( x0 + y, y0 + x, color)
        fbuf.pixel( x0 - y, y0 + x, color)
        fbuf.pixel( x0 - x, y0 + y, color)
        fbuf.pixel( x0 - x, y0 - y, color)
        fbuf.pixel( x0 - y, y0 - x, color)
        fbuf.pixel( x0 + y, y0 - x, color)
        fbuf.pixel( x0 + x, y0 - y, color)

        y += 1
        if err < 0:
            err += 2 * y + 1
        else:
            x -= 1
            err += 2 * (y - x + 1)

def draw_filled_circle(fbuf, x0: int, y0: int, r: int, color: int):
    """
    Draw a filled circle by drawing horizontal lines between the circle’s edges.
    fbuf: the SSD1306 display object (framebuffer)
    (x0, y0): center
    r: radius
    color: 1 = white, 0 = black
    """
    for dy in range(-r, r + 1):
        dx = int(math.sqrt(r * r - dy * dy))
        x_start = x0 - dx
        # width of horizontal line = (x0+dx) - (x0-dx) + 1 = 2*dx + 1
        width = 2 * dx + 1
        y = y0 + dy
        # draw a horizontal line of length width at vertical position y
        fbuf.fill_rect(x_start, y, width, 1, color)

# ──────────────────────────────────────────────────────────────────────────────


# ──────────────────────────────────────────────────────────────────────────────
# SET UP I²C AND SSD1306 DISPLAY
# ──────────────────────────────────────────────────────────────────────────────

# On Pico W, SDA = GP0, SCL = GP1 for default I2C
i2c = busio.I2C(scl=board.GP1, sda=board.GP0)
oled = adafruit_ssd1306.SSD1306_I2C(
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    i2c,
    addr=0x3C,      # SSD1306 I²C address (usually 0x3C or 0x3D)
)

# Clear display buffer initially
oled.fill(0)
oled.show()

# ──────────────────────────────────────────────────────────────────────────────
# MAIN ANIMATION LOOP 
# ──────────────────────────────────────────────────────────────────────────────
angle_deg = 0.0

while True:
    # 1) Clear the OLED buffer
    oled.fill(0)

    # 2) Draw the electron's circular orbit (outline)
    draw_circle_outline(oled, center_x, center_y, orbit_radius, 1)

    # 3) Draw the nucleus (three filled circles)
    draw_filled_circle(oled, center_x, center_y, nucleus_radius, 1)
    draw_filled_circle(oled, center_x - offset, center_y + offset, nucleus_radius, 1)
    draw_filled_circle(oled, center_x + offset, center_y + offset, nucleus_radius, 1)

    # 4) Compute the electron’s position along its orbit
    theta = math.radians(angle_deg)
    electron_x = center_x + int(round(orbit_radius * math.cos(theta) )  )
    electron_y = center_y + int(round(orbit_radius * math.sin(theta) )  )

    # 5) Draw the electron as a filled circle
    draw_filled_circle(oled, electron_x, electron_y, electron_radius, 1)

    # 6) Send the buffer to the OLED
    oled.show()

    # 7) Advance the angle for the next frame
    angle_deg += angle_increment
    if angle_deg >= 360.0:
        angle_deg -= 360.0

    # 8) Delay as much as you like/want
    time.sleep(frame_delay)
# ──────────────────────────────────────────────────────────────────────────────