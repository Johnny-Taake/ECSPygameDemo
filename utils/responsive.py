"""Responsive design utilities for maintaining fixed aspect ratio."""


class ResponsiveScaleManager:
    def __init__(self, base_width=640, base_height=400):
        self.base_width = base_width
        self.base_height = base_height

        self.window_width = base_width
        self.window_height = base_height

        self.scale = 1.0
        self.offset_x = 0
        self.offset_y = 0

    def update_window_size(self, width, height):
        self.window_width = width
        self.window_height = height

        target_ratio = self.base_width / self.base_height
        window_ratio = width / height

        if window_ratio > target_ratio:
            # Window is wider → limited by height
            self.scale = height / self.base_height
            render_w = int(self.base_width * self.scale)
            self.offset_x = (width - render_w) // 2
            self.offset_y = 0
        else:
            # Window is narrower → limited by width
            self.scale = width / self.base_width
            render_h = int(self.base_height * self.scale)
            self.offset_x = 0
            self.offset_y = (height - render_h) // 2

    def world_to_screen(self, x, y):
        return (
            int(self.offset_x + x * self.scale),
            int(self.offset_y + y * self.scale),
        )

    def screen_to_world(self, x, y):
        return (
            (x - self.offset_x) / self.scale,
            (y - self.offset_y) / self.scale,
        )
