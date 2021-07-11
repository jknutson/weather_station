import sys
import os
picdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pic')
libdir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in66
from PIL import Image,ImageDraw,ImageFont

class Display:
    # Display instruction types
    DISP_TYPE_TEXT = 1
    DISP_TYPE_LINE = 2
    DISP_TYPE_ARC = 3
    DISP_TYPE_CHORD = 4
    DISP_TYPE_RECT = 5

    # Screen Orientation
    DISP_LAYOUT_LANDSCAPE = 1
    DISP_LAYOUT_PORTRAIT = 2

    def __init__(self) -> None:
        self.draw_functions = {
            self.DISP_TYPE_TEXT: self.drawtext, 
            self.DISP_TYPE_LINE: self.drawline, 
            self.DISP_TYPE_ARC: self.drawarc, 
            self.DISP_TYPE_CHORD: self.drawchord, 
            self.DISP_TYPE_RECT: self.drawrect
            }
        self.epd = epd2in66.EPD()
        self.epd.init(0)
        self.font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        self.font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)

    def clear(self):
        self.epd.Clear()

    def new_canvas(self, orientation):
        self.orientation = orientation
        layout = self.get_canvas_size(self.orientation)
        self.Himage = Image.new('1', layout, 0xFF)  # 0xFF: clear the frame
        self.draw = ImageDraw.Draw(self.Himage)

    def get_canvas_size(self, orientation):
        return (self.epd.height, self.epd.width) if orientation == self.DISP_LAYOUT_LANDSCAPE else (self.epd.width, self.epd.height)

    def finish_drawing(self):
        self.epd.display(self.epd.getbuffer(self.Himage))

    def draw(self, orientation, instructions):
        self.new_canvas(orientation)
        for instruciton in instructions:
            self.draw_functions[instruciton[0]](instruciton[1], instruciton[2], instruciton[3])
        self.finish_drawing()
    
    def drawtext(self, coords, p_parms, k_parms):
        self.draw.text(coords, *p_parms, **k_parms)

    def drawline(self, coords, p_parms, k_parms):
        self.draw.line(coords, **k_parms)

    def drawarc(self, coords, p_parms, k_parms):
        self.draw.arc(coords, *p_parms, **k_parms)

    def drawchord(self, coords, p_parms, k_parms):
        self.draw.chord(coords, *p_parms, **k_parms)

    def drawrect(self, coords, p_parms, k_parms):
        self.draw.rectangle(coords, **k_parms)

    @staticmethod
    def create_instruction(type, coords, p_parms, k_parms):
        return (type, coords, p_parms, k_parms)
