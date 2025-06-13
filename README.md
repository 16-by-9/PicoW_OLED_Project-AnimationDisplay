# OLED Animation Display on the Raspberry Pi Pico W (CircuitPython)

This project shows how to use a Raspberry Pi Pico W running **CircuitPython** to display animated graphics on a 128×64 OLED screen using the **Adafruit SSD1306** library.

---

## 💾 Requirements

### ✅ Hardware
- Raspberry Pi Pico W
- 128x64 OLED screen (I2C, SSD1306 driver)
- Jumper wires

### 🧠 Software / Libraries

This is a **CircuitPython** project. **This will NOT work with Arduino or MicroPython.**

#### Required libraries (copy into `/lib` on the `CIRCUITPY` drive):
- `adafruit_ssd1306.mpy`
- `adafruit_framebuf.mpy`
- `adafruit_display_text`
- `adafruit_gfx`
- `adafruit_cursorcontrol`

#### Optional but useful:
- `adafruit_display_shapes` (for drawing shapes)
- `adafruit_led_animation` (if you want flashy blinky stuff later)
- `adafruit_io` (for future internety integrations)

#### Fonts:
You need to also drop in:
- `font5x8.bin` — put this directly in the root of `CIRCUITPY` or `/lib` depending on your code

---

## 🔥 Setting up CircuitPython on Pico W

1. Go to https://circuitpython.org/board/raspberry_pi_pico_w/
2. Download the latest `.uf2` file.
3. Hold the **BOOTSEL** button while plugging in your Pico W.
4. Drag and drop the `.uf2` file to the `RPI-RP2` drive that shows up.
5. It will reboot and show as a new drive named `CIRCUITPY`.

Done!

---

## 📸 Image Display Notes

If you're displaying a bitmap image (`image.bmp`):

- Must be exactly `128x64` pixels
- Must be **1-bit depth** (black and white only)
- Must be saved as **uncompressed BMP**
- You can use [GIMP](https://www.gimp.org/) or Photoshop to convert

**GIMP Conversion Tip:**
1. Open your PNG/JPG in GIMP
2. `Image > Mode > Indexed`
3. Choose "Use black and white (1-bit) palette"
4. `File > Export As...` → choose `image.bmp`
5. Make sure to export as **Windows BMP** with **no compression**

The code will expect the file to be named **`image.bmp`**, placed in the root of the `CIRCUITPY` drive.

---

### ⚛️ Animated Atom Simulation

A minimal atomic model with:
- Nucleus with 3 clustered nucleons
- Orbiting electron (drawn frame by frame)
- Runs smoothly with simple trigonometry

Loop animation rotates the electron around the nucleus. Your OLED becomes a tiny particle accelerator!

---

### 🖼️ Bitmap Display Code

Reads a `128x64` bitmap and draws it on screen using `displayio` and `OnDiskBitmap`.

Make sure you’ve named your image exactly `image.bmp`.

---

## ⚠️ Known Problems

- OLED won’t work unless wiring is correct (SDA, SCL, and VCC *securely* connected)
- If you forget to switch from your PC's Python to CircuitPython in Thonny, you'll see `no module named board` (LOL)
- CircuitPython storage is tiny. Think Apollo 11-era tiny. Remove unused libraries when done.

---

## 📂 Folder Structure

CIRCUITPY/
├── code.py
├── image.bmp
├── font5x8.bin
└── lib/
├── adafruit_ssd1306.mpy
├── adafruit_framebuf.mpy
├── adafruit_display_text/
├── adafruit_gfx.mpy
├── adafruit_cursorcontrol/
└── adafruit_display_shapes/ ← optional
