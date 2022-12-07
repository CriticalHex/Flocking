class Color:
    def __init__(self):
        self.r, self.g, self.b = 0,0,0
        self.r_speed, self.g_speed, self.b_speed = 1,3,2
        self.r_dir, self.g_dir, self.b_dir = 1, 1, 1
        
    def inc(self):
        self.r += self.r_dir * self.r_speed
        self.g += self.g_dir * self.g_speed
        self.b += self.b_dir * self.b_speed

        # Check if any of the color values have reached the maximum or minimum
        if self.r >= 255:
            self.r = 255
            self.r_dir = -1
        elif self.r <= 0:
            self.r = 0
            self.r_dir = 1

        if self.g >= 255:
            self.g = 255
            self.g_dir = -1
        elif self.g <= 0:
            self.g = 0
            self.g_dir = 1

        if self.b >= 255:
            self.b = 255
            self.b_dir = -1
        elif self.b <= 0:
            self.b = 0
            self.b_dir = 1
    
    def get_color(self):
        return self.r, self.g, self.b