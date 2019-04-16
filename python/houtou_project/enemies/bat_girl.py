""" The class BatGirl"""
from bullet import Bullet, GeneralSniperBullet
from bullet_settings import BulletSettings
from shape import Circle
from enemies.enemy import Enemy


class BatGirl(Enemy):
    """ The boss - bat girl!"""
    def __init__(self, screen, image_path, center, hit_point):
        super().__init__(screen, image_path, center, hit_point)
        self.bullet1_circle = Circle(
            color_edge=(25, 140, 255),
            color_inside=(255, 255, 255),
            radius=3, width=1)
        self.bullet1_settings = BulletSettings(self.bullet1_circle.image,
                                               255, 6)

    def check_ticks(self, player): # pylint: disable=W0221
        if self.ticks % 30 == 0:
            new_bullet = Bullet(self.screen, self.bullet1_settings,
                                self.rect.center, 90)
            self.bullets.add(new_bullet)
            new_bullets = GeneralSniperBullet(self.screen,
                                              self.bullet1_settings, self,
                                              player, 120, 3)
            for bullet in new_bullets:
                self.bullets.add(bullet)
        self.ticks += 1
