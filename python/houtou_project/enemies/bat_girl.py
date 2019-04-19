""" The class BatGirl"""
# TODO: GeneralSniperBullet
# from bullet import Bullet, GeneralSniperBullet
from bullet import Bullet
from enemies.enemy import Enemy
from motion import UniformlyAcceleratedLinearMotion
from shape import CircleShape


class BatGirl(Enemy):
    """ The boss - bat girl!"""
    def __init__(self, screen, image_path, center, hit_point):
        super().__init__(screen, image_path, center, hit_point)
        self.bullet1_circle = CircleShape(
            alpha=255,
            color_edge=(25, 140, 255),
            color_inside=(255, 255, 255),
            radius=3, width=1, screen=screen)

    def check_ticks(self, player): # pylint: disable=W0221
        # TODO: GeneralSniperBullet
        if self.ticks % 30 == 0:
            new_bullet = Bullet(
                self.rect.center,
                shape_type='CircleShape',
                alpha=255,
                color_edge=(25, 140, 255),
                color_inside=(255, 255, 255),
                radius=3,
                width=1,
                screen=self.screen,
                motion_type='UniformlyAcceleratedLinearMotion',
                speed=6,
                acceleration=0,
                degree=90)
            self.bullets.add(new_bullet)
            # new_bullets = GeneralSniperBullet(self.screen,
            #                                   self.bullet1_settings, self,
            #                                   player, 120, 3)
            # for bullet in new_bullets:
            #     self.bullets.add(bullet)
        self.ticks += 1
