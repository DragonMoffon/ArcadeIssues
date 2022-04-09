import arcade


class NinePatch:

    def __init__(self, center_x, center_y, width, height, scale):
        self.t_l = arcade.Sprite("Corner.png", scale=scale)
        self.t_l.center_x = center_x - width / 2 - 16 * scale
        self.t_l.center_y = center_y + height / 2 + 16 * scale

        self.t_r = arcade.Sprite("Corner.png", angle=270, scale=scale)
        self.t_r.center_x = center_x + width / 2 + 16 * scale
        self.t_r.center_y = center_y + height / 2 + 16 * scale

        self.b_r = arcade.Sprite("Corner.png", angle=180, scale=scale)
        self.b_r.center_x = center_x + width / 2 + 16 * scale
        self.b_r.center_y = center_y - height / 2 - 16 * scale

        self.b_l = arcade.Sprite("Corner.png", angle=90, scale=scale)
        self.b_l.center_x = center_x - width / 2 - 16 * scale
        self.b_l.center_y = center_y - height / 2 - 16 * scale

        self.t = arcade.Sprite("Center.png", scale=scale,
                               center_x=center_x, center_y=center_y + height / 2 + 16 * scale)
        self.t.width = width
        self.l = arcade.Sprite("Center.png", scale=scale,
                               center_x=center_x - width / 2 - 16 * scale, center_y=center_y)
        self.l.height = height
        self.b = arcade.Sprite("Center.png", scale=scale,
                               center_x=center_x, center_y=center_y - height / 2 - 16 * scale)
        self.b.width = width
        self.r = arcade.Sprite("Center.png", scale=scale,
                               center_x=center_x + width / 2 + 16 * scale, center_y=center_y)
        self.r.height = height

        self.body = arcade.Sprite("Center.png", center_x=center_x, center_y=center_y, scale=scale)
        self.body.width = width
        self.body.height = height

        self.renderer = arcade.SpriteList()
        self.renderer.extend([self.t_r, self.t_l, self.b_r, self.b_l,
                              self.t, self.l, self.b, self.r, self.body])

    def draw(self):
        self.renderer.draw(pixelated=True)
        self.renderer.draw_hit_boxes(arcade.color.LIME_GREEN)

    def drag(self, x, y, dx, dy):
        p = (x, y)
        if self.body.collides_with_point(p):
            self.renderer.move(dx, dy)
        elif self.t.collides_with_point(p):
            self.t.center_y += dy
            self.t_l.center_y += dy
            self.t_r.center_y += dy

            self.l.center_y += dy / 2
            self.l.height += dy

            self.r.center_y += dy / 2
            self.r.height += dy

            self.body.center_y += dy / 2
            self.body.height += dy

        elif self.t_l.collides_with_point(p):
            self.t_l.center_x += dx
            self.t_l.center_y += dy

            self.t.center_y += dy
            self.t.center_x += dx / 2
            self.t.width -= dx

            self.t_r.center_y += dy

            self.r.center_y += dy / 2
            self.r.height += dy

            self.b_l.center_x += dx

            self.b.center_x += dx / 2
            self.b.width -= dx

            self.l.center_x += dx
            self.l.center_y += dy / 2
            self.l.height += dy

            self.body.center_x += dx / 2
            self.body.center_y += dy / 2
            self.body.width -= dx
            self.body.height += dy
