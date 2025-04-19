from settings import *

class SegHandler:
    def __init__(self, engine):
        self.engine = engine
        self.wad_data = engine.wad_data
        self.player = engine.player
        
        self.seg = None
        self.rw_angle1 = None

    def update(self):
        self.init_screen_range()

    def draw_solid_wall_range(self, x1, x2):
        self.engine.view_renderer.draw_vline(x1, 0, HEIGHT)
        
    def init_screen_range(self):
        self.screen_range = set(range(WIDTH))

    def clip_solid_walls(self, x_start, x_end):
        if self.screen_range:
            curr_wall = set(range(x_start, x_end))
            intersection = curr_wall & self.screen_range

            if intersection and len(intersection) == len(curr_wall):
                self.draw_solid_wall_range(x_start, x_end - 1)
            else:
                arr = sorted(intersection)
                if arr:
                    x, x2 = arr[0], arr[-1]
                    for x1, x2 in zip(arr, arr[1:]):
                        if x2 - x1 > 1:
                            self.draw_solid_wall_range(x, x1)
                            x = x2
                    self.draw_solid_wall_range(x, x2)
            self.screen_range -= intersection
        else:
            self.engine.bsp.is_traverse_bsp = False

    def classify_segment(self, segment, x1, x2, rw_angle1):
        self.seg = segment
        self.rw_angle1 = rw_angle1

        if x1 == x2:
            return None
        
        back_sector = segment.back_sector
        front_sector = segment.front_sector

        if back_sector is None:
            self.clip_solid_walls(x1, x2)
            return None