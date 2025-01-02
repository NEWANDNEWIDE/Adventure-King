import pygame.event
import pytmx.util_pygame
import game_master
import game_player.player
import items.className
import npc.boss
import settings
from game_master.gameSurface import GameSprite


class Map:
    """这个类是用来交作业的"""
    def __init__(self, screen):
        self.tmx = pytmx.util_pygame.load_pygame(settings.MAP)
        self.__ui_state = game_player.player.State()
        self.__item = game_master.item.Item()
        self.__state = 1
        self.__screen = screen
        self.__stop = 0
        self.boss_map = 0
        self.boss = None

        self.collision = pygame.sprite.Group()
        self.attack_collision = pygame.sprite.Group()
        self.attacking_collision = pygame.sprite.Group()

        self.boss_collision = pygame.sprite.Group()
        self.boss_attack_collision = pygame.sprite.Group()
        self.boss_attacking_collision = pygame.sprite.Group()

        self.boss_camera = game_player.player.CameraGroup(pygame.Surface((1600, 1200)), pytmx.util_pygame.load_pygame("res/map/first_map/boss.tmx"), self.boss_collision)
        self.camera = game_player.player.CameraGroup(pygame.Surface((8000, 8000)), self.tmx, self.collision)
        self.player = game_player.player.Player([431, 7638], self.collision, self.boss_collision, self.camera, self.boss_camera)

        self.pick_up = game_master.gameSurface.PickUpSpritesGroup(self.player)
        self.boss_pick_up = game_master.gameSurface.PickUpSpritesGroup(self.player)

        self.__item = Item(self.player)

        self.inventory_rect = self.player.bag.inventory_rect

        self.object = []
        self.goods = []
        self.losing = []

        self.boss_object = []
        self.boss_goods = []
        self.boss_losing = []

        self.object.append(self.player)

        self.setup()

        self.player.bag.put(items.className.GOODS[items.weapons.Sword.NAME]())
        self.player.bag.put(items.className.GOODS[items.armors.IronArmor.NAME]())
        self.player.bag.put(items.className.GOODS[items.armors.IronBoots.NAME]())
        self.player.bag.put(items.className.GOODS[items.armors.IronHelmet.NAME]())
        self.add_obj(npc.monster.Goblin([350, 7630], self.collision, self.camera, self.attack_collision))

        self.load_boss_map()

    def load_boss_map(self):
        self.boss_map = 1
        self.__item.boss = 1
        t = self.player.boss_spawn_point.copy()
        self.player.boss = 1
        self.player.attribute.rect = t
        self.player.rect.center = t
        self.player.hitbox.center = t
        self.player.h_n = self.player.attribute_now.health
        self.player.s_n = self.player.attribute_now.shield
        self.boss = npc.boss.Crazy([1263, 558], self.boss_collision, self.boss_camera, self.boss_attack_collision)
        self.add_obj(self.boss)
        self.boss_object.append(self.player)

    def add_obj(self, obj):
        if self.boss_map:
            self.boss_attack_collision.add(obj)
            self.boss_object.append(obj)
            return
        self.attack_collision.add(obj)
        self.object.append(obj)

    def add_losing(self, obj):
        obj = GameSprite(obj, self.camera, self.pick_up)
        if self.boss_map:
            self.boss_losing.append(obj)
            return
        self.losing.append(obj)

    def add_goods(self, obj):
        if self.boss_map:
            self.boss_collision.add(obj)
            self.boss_goods.append(obj)
            return
        self.collision.add(obj)
        self.goods.append(obj)

    def throwing(self, losing):
        losing.rect = self.player.attribute.rect.copy()
        if self.player.move_state[-5:] == "front":
            losing.vec2[1] = -1
        elif self.player.move_state[-4:] == "back":
            losing.vec2[1] = 1
        elif self.player.move_state[-4:] == "left":
            losing.vec2[0] = -1
        elif self.player.move_state[-5:] == "right":
            losing.vec2[0] = 1
        self.add_losing(losing)

    def move(self, losing, dt):
        losing.attribute.rect[0] += 400 * losing.attribute.vec2[0] * dt
        losing.attribute.rect[1] += 400 * losing.attribute.vec2[1] * dt
        return losing.attribute.rect

    @staticmethod
    def get_rect_x(obj):
        return obj.attribute.rect[0]

    @staticmethod
    def get_rect_y(obj):
        return obj.attribute.rect[1]

    def sort_losing(self):
        self.losing.sort(key=Map.get_rect_x)

    def sort_object(self):
        self.object.sort(key=Map.get_rect_y)

    def set_name(self, name: str):
        self.player.attribute.name = name

    def setup(self):
        game_master.synthesis.PLAYER_SYNTHESIS_LIST = game_master.synthesis.process(
            game_master.synthesis.PLAYER_SYNTHESIS_LIST_NOT_PROCESSED)
        game_master.synthesis.SYNTHESIS_LIST = game_master.synthesis.process(
            game_master.synthesis.SYNTHESIS_LIST_NOT_PROCESSED, 3)

    def event_update(self, event: pygame.event.Event):
        if self.__stop:
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    self.__stop = 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.__stop = self.__item.action(pygame.mouse.get_pos())
        elif self.__state and not self.player.dead:
            if event.type == pygame.KEYDOWN:
                if event.key == 27:
                    self.__stop = 1
                elif event.key == pygame.K_b:
                    if self.player.bag.state:
                        self.player.bag.close()
                    elif not self.player.sys_state:
                        self.player.bag.open()
                elif 48 <= event.key <= 57:
                    if event.key == 48:
                        self.player.bag.selection_box = 43
                    elif self.player.bag.selection_box != event.key - 48:
                        self.player.bag.selection_box = event.key - 15
                    self.player.bag.update_inventory()
                elif event.key == pygame.K_e:
                    if not self.player.bag.state and not self.player.sys_state and self.player.bag.bag[self.player.bag.selection_box]:
                        if isinstance(self.player.bag.bag[self.player.bag.selection_box], game_master.synthesis.Synthesis):
                            self.player.sys_state = self.player.bag.bag[self.player.bag.selection_box].open()
                    elif self.player.sys_state:
                        self.player.sys_state = self.player.sys_state.close()
                elif event.key == 1073742049:
                    self.player.run = 0 if self.player.run else 1
                elif event.key == 32 and not self.player.shanbi_state and self.player.shanbi >= 0 and (
                        self.player.vec2[0] or self.player.vec2[1]) and not self.player.attacking:
                    self.player.shanbi_state = 1
                    self.player.shanbi = 0.1
                    self.player.dir = self.player.vec2.copy()
                if not self.player.attacking:
                    if event.key == pygame.K_w:
                        self.player.vec2 = [0, -1]
                    elif event.key == pygame.K_s:
                        self.player.vec2 = [0, 1]
                    elif event.key == pygame.K_a:
                        self.player.vec2 = [-1, 0]
                    elif event.key == pygame.K_d:
                        self.player.vec2 = [1, 0]
            elif event.type == pygame.KEYUP:
                pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                pos = list(pos)
                if not self.player.bag.state and not self.player.sys_state:
                    if (self.inventory_rect[0] + 2 <= pos[0] <= self.inventory_rect[0] + 420 and
                            self.inventory_rect[1] + 2 <= pos[1] <= self.inventory_rect[1] + 42):
                        pos[0] -= self.inventory_rect[0] + 2
                        i = 0
                        for i in range(10):
                            pos[0] -= 40
                            if pos[0] <= 0:
                                break
                            elif 0 < pos[0] < 2:
                                i = -1
                                break
                            pos[0] -= 2
                        if i + 1 and self.player.bag.selection_box != 34 + i:
                            self.player.bag.selection_box = 34 + i
                            self.player.bag.update_inventory()
                            return
                if event.button == pygame.BUTTON_LEFT:
                    if self.player.bag.state:
                        t = self.player.bag.selected(pos, pygame.BUTTON_LEFT)
                        if t:
                            self.throwing(t)
                    elif self.player.sys_state:
                        t = self.player.sys_state.selected(pos, pygame.BUTTON_LEFT)
                        if t:
                            self.throwing(t)
                    else:
                        if not self.player.attacking:
                            self.player.attacking = 1
                            self.player.move_state = "attack_" + self.player.move_state.split('_')[1]
                            self.player.index = 0
                            self.player.vec2 = [0, 0]
                            if self.boss_map:
                                self.player.attack(self.boss_attacking_collision)
                            else:
                                self.player.attack(self.attacking_collision)
                elif event.button == pygame.BUTTON_RIGHT:
                    if self.player.bag.state:
                        t = self.player.bag.selected(pos, pygame.BUTTON_RIGHT)
                        if t:
                            self.throwing(t)
                    elif self.player.sys_state:
                        t = self.player.sys_state.selected(pos, pygame.BUTTON_RIGHT)
                        if t:
                            self.throwing(t)
                    else:
                        self.player.use()
                elif event.button == 4:
                    self.player.bag.selection_box += 1
                    self.player.bag.update_inventory()
                elif event.button == 5:
                    self.player.bag.selection_box -= 1
                    self.player.bag.update_inventory()

    def update_losing(self, dt):
        if self.boss_map:
            l = len(self.boss_losing)
            for i in range(l):
                if -1600 <= self.player.rect.centerx - self.boss_losing[i].rect.centerx <= 1600 and -1450 <= self.player.rect.centery - self.boss_losing[i].rect.centery <= 1450:
                    if self.boss_losing[i].attribute.time > 299.7:
                        self.boss_losing[i].attribute.rect = self.move(self.boss_losing[i], dt)
                        self.boss_losing[i].rect.center = self.boss_losing[i].attribute.rect
                    self.boss_losing[i].attribute.time -= dt
                    if self.boss_losing[i].time > 0:
                        self.boss_losing[i].time -= dt
                    if self.boss_losing[i].attribute.time <= 0:
                        self.boss_camera.remove(self.boss_losing[i][0])
                        del self.boss_losing[i]
                    if self.boss_losing[i].time <= 0 and not self.boss_losing[i].get:
                        self.boss_losing[i].get = 1
        else:
            l = len(self.losing)
            for i in range(l):
                if -1600 <= self.player.rect.centerx - self.losing[i].rect.centerx <= 1600 and -1450 <= self.player.rect.centery - self.losing[i].rect.centery <= 1450:
                    if self.losing[i].attribute.time > 299.7:
                        self.losing[i].attribute.rect = self.move(self.losing[i], dt)
                        self.losing[i].rect.center = self.losing[i].attribute.rect
                    self.losing[i].attribute.time -= dt
                    if self.losing[i].time > 0:
                        self.losing[i].time -= dt
                    if self.losing[i].attribute.time <= 0:
                        self.camera.remove(self.losing[i][0])
                        del self.losing[i]
                    if self.losing[i].time <= 0 and not self.losing[i].get:
                        self.losing[i].get = 1

    def update_goods(self, dt):
        pass

    def update_object(self, dt):
        if self.boss_map:
            for o in range(len(self.boss_object)):
                if -1400 <= self.player.rect.centerx - self.boss_object[o].rect.centerx <= 1400 and -1050 <= self.player.rect.centery - self.boss_object[o].rect.centery <= 1050:
                    if isinstance(self.boss_object[o], game_player.player.Player):
                        self.__item.d = self.boss_object[o].update(dt)
                        self.__stop = self.__item.d
                    elif isinstance(self.boss_object[o], game_master.gameObject.GameNpc):
                        t = self.boss_object[o].update(dt, self.boss_attacking_collision, self.player.rect)
                        if t:
                            self.boss_camera.remove(t)
                            self.boss_attack_collision.remove(t)
        else:
            for o in range(len(self.object)):
                if -1400 <= self.player.rect.centerx - self.object[o].rect.centerx <= 1400 and -1050 <= self.player.rect.centery - self.object[o].rect.centery <= 1050:
                    if isinstance(self.object[o], game_player.player.Player):
                        self.__item.d = self.object[o].update(dt)
                        self.__stop = self.__item.d
                    elif isinstance(self.object[o], game_master.gameObject.GameNpc):
                        t = self.object[o].update(dt, self.attacking_collision, self.player.rect)
                        if t:
                            self.camera.remove(t)
                            self.attack_collision.remove(t)

    def update_collision(self):
        if self.boss_map:
            for sprite in self.boss_attack_collision.sprites():
                if hasattr(sprite, "hitbox"):
                    if self.player.hitbox.colliderect(sprite.hitbox):
                        if sprite.vec2[0] or sprite.vec2[1]:
                            if sprite.vec2[0] == -1:
                                sprite.hitbox.left = self.player.hitbox.right
                                sprite.rect.centerx = sprite.hitbox.centerx
                                sprite.attribute.rect[0] = sprite.hitbox.centerx
                            elif sprite.vec2[0] == 1:
                                sprite.hitbox.right = self.player.hitbox.left
                                sprite.rect.centerx = sprite.hitbox.centerx
                                sprite.attribute.rect[0] = sprite.hitbox.centerx
                            elif sprite.vec2[1] == -1:
                                sprite.hitbox.top = self.player.hitbox.bottom
                                sprite.rect.centery = sprite.hitbox.centery
                                sprite.attribute.rect[1] = sprite.hitbox.centery
                            elif sprite.vec2[1] == 1:
                                sprite.hitbox.bottom = self.player.hitbox.top
                                sprite.rect.centery = sprite.hitbox.centery
                                sprite.attribute.rect[1] = sprite.hitbox.centery
                        else:
                            if self.player.vec2[0] == -1:
                                self.player.hitbox.left = sprite.hitbox.right
                                self.player.rect.centerx = self.player.hitbox.centerx
                                self.player.attribute.rect[0] = self.player.hitbox.centerx
                            elif self.player.vec2[0] == 1:
                                self.player.hitbox.right = sprite.hitbox.left
                                self.player.rect.centerx = self.player.hitbox.centerx
                                self.player.attribute.rect[0] = self.player.hitbox.centerx
                            elif self.player.vec2[1] == -1:
                                self.player.hitbox.top = sprite.hitbox.bottom
                                self.player.rect.centery = self.player.hitbox.centery
                                self.player.attribute.rect[1] = self.player.hitbox.centery
                            elif self.player.vec2[1] == 1:
                                self.player.hitbox.bottom = sprite.hitbox.top
                                self.player.rect.centery = self.player.hitbox.centery
                                self.player.attribute.rect[1] = self.player.hitbox.centery
        else:
            for sprite in self.attack_collision.sprites():
                if hasattr(sprite, "hitbox"):
                    if self.player.hitbox.colliderect(sprite.hitbox):
                        if sprite.vec2[0] or sprite.vec2[1]:
                            if sprite.vec2[0] == -1:
                                sprite.hitbox.left = self.player.hitbox.right
                                sprite.rect.centerx = sprite.hitbox.centerx
                                sprite.attribute.rect[0] = sprite.hitbox.centerx
                            elif sprite.vec2[0] == 1:
                                sprite.hitbox.right = self.player.hitbox.left
                                sprite.rect.centerx = sprite.hitbox.centerx
                                sprite.attribute.rect[0] = sprite.hitbox.centerx
                            elif sprite.vec2[1] == -1:
                                sprite.hitbox.top = self.player.hitbox.bottom
                                sprite.rect.centery = sprite.hitbox.centery
                                sprite.attribute.rect[1] = sprite.hitbox.centery
                            elif sprite.vec2[1] == 1:
                                sprite.hitbox.bottom = self.player.hitbox.top
                                sprite.rect.centery = sprite.hitbox.centery
                                sprite.attribute.rect[1] = sprite.hitbox.centery
                        else:
                            if self.player.vec2[0] == -1:
                                self.player.hitbox.left = sprite.hitbox.right
                                self.player.rect.centerx = self.player.hitbox.centerx
                                self.player.attribute.rect[0] = self.player.hitbox.centerx
                            elif self.player.vec2[0] == 1:
                                self.player.hitbox.right = sprite.hitbox.left
                                self.player.rect.centerx = self.player.hitbox.centerx
                                self.player.attribute.rect[0] = self.player.hitbox.centerx
                            elif self.player.vec2[1] == -1:
                                self.player.hitbox.top = sprite.hitbox.bottom
                                self.player.rect.centery = self.player.hitbox.centery
                                self.player.attribute.rect[1] = self.player.hitbox.centery
                            elif self.player.vec2[1] == 1:
                                self.player.hitbox.bottom = sprite.hitbox.top
                                self.player.rect.centery = self.player.hitbox.centery
                                self.player.attribute.rect[1] = self.player.hitbox.centery

    def update_attack(self, dt):
        if self.boss_map:
            if not self.player.shanbi_state:
                for sprite in self.boss_attacking_collision.sprites():
                    if sprite.time != -1:
                        sprite.time -= dt
                        if sprite.time <= 0:
                            self.boss_attacking_collision.remove(sprite)
                            continue
                    if sprite.rect.colliderect(self.player.rect):
                        if sprite.who != "player":
                            if self.player.attribute_now.defense < sprite.damage:
                                sprite.damage -= self.player.attribute_now.defense
                                self.player.damage_a = sprite.damage
                                if self.player.s_n:
                                    if self.player.s_n >= sprite.damage:
                                        self.player.s_n -= sprite.damage
                                    else:
                                        self.player.h_n += self.player.s_n - sprite.damage
                                        self.player.s_n = 0
                                else:
                                    self.player.h_n -= sprite.damage
                            else:
                                self.player.damage_a = 0
                            self.player.damage_t = 1
                            self.boss_attacking_collision.remove(sprite)
            for sprite in self.boss_attacking_collision.sprites():
                if sprite.time != -1:
                    sprite.time -= dt
                    if sprite.time <= 0:
                        self.boss_attacking_collision.remove(sprite)
                        continue
                for obj in self.boss_attack_collision.sprites():
                    if sprite.rect.colliderect(obj.rect):
                        if obj.can_be_attack and sprite.who == "player":
                            if obj.attribute_now.defense < sprite.damage:
                                sprite.damage -= obj.attribute_now.defense
                                obj.damage_a = sprite.damage
                                if obj.s_n:
                                    if obj.s_n >= sprite.damage:
                                        obj.s_n -= sprite.damage
                                    else:
                                        obj.h_n += obj.s_n - sprite.damage
                                        obj.s_n = 0
                                else:
                                    obj.h_n -= sprite.damage
                            else:
                                obj.damage_a = 0
                            obj.damage_t = 1
                            self.boss_attacking_collision.remove(sprite)
        else:
            if not self.player.shanbi_state:
                for sprite in self.attacking_collision.sprites():
                    if sprite.time != -1:
                        sprite.time -= dt
                        if sprite.time <= 0:
                            self.attacking_collision.remove(sprite)
                            continue
                    if sprite.rect.colliderect(self.player.rect):
                        if sprite.who != "player":
                            if self.player.attribute_now.defense < sprite.damage:
                                sprite.damage -= self.player.attribute_now.defense
                                self.player.damage_a = sprite.damage
                                if self.player.s_n:
                                    if self.player.s_n >= sprite.damage:
                                        self.player.s_n -= sprite.damage
                                    else:
                                        self.player.h_n += self.player.s_n - sprite.damage
                                        self.player.s_n = 0
                                else:
                                    self.player.h_n -= sprite.damage
                            else:
                                self.player.damage_a = 0
                            self.player.damage_t = 1
                            self.attacking_collision.remove(sprite)
            for sprite in self.attacking_collision.sprites():
                if sprite.time != -1:
                    sprite.time -= dt
                    if sprite.time <= 0:
                        self.attacking_collision.remove(sprite)
                        continue
                for obj in self.attack_collision.sprites():
                    if sprite.rect.colliderect(obj.rect):
                        if obj.can_be_attack and sprite.who == "player":
                            if obj.attribute_now.defense < sprite.damage:
                                sprite.damage -= obj.attribute_now.defense
                                obj.damage_a = sprite.damage
                                if obj.s_n:
                                    if obj.s_n >= sprite.damage:
                                        obj.s_n -= sprite.damage
                                    else:
                                        obj.h_n += obj.s_n - sprite.damage
                                        obj.s_n = 0
                                else:
                                    obj.h_n -= sprite.damage
                            else:
                                obj.damage_a = 0
                            obj.damage_t = 1
                            self.attacking_collision.remove(sprite)

    def update(self, dt):
        if self.__stop:
            if not self.__item.state:
                self.__stop = 0
            return self.__item.state
        self.update_losing(dt)
        self.update_object(dt)
        self.update_goods(dt)
        self.update_collision()
        self.update_attack(dt)
        if self.boss_map:
            self.boss_pick_up.update(self.losing, self.camera)
            self.boss_camera.update(self.player.rect.bottom)
        else:
            self.pick_up.update(self.losing, self.camera)
            self.camera.update(self.player.rect.bottom)
        return 1

    def render_UI(self):
        if self.boss_map:
            if self.boss:
                text = pygame.font.Font(settings.FONT, 20).render(self.boss.name, True, (0, 0, 0))
                rect = text.get_rect(center=(600, 50))
                pygame.display.get_surface().blit(text, rect)
                s = pygame.Surface((210, 30))
                s_rect = s.get_rect(center=rect.center)
                s_rect.top = rect.bottom
                s.fill((255, 255, 255))
                p = self.boss.h_n / self.boss.attribute_now.health
                if p * 200 >= 1:
                    surf = pygame.surface.Surface((p * 200, 20))
                    surf.fill((255, 0, 0))
                    s.blit(surf, (5, 5))
                pygame.display.get_surface().blit(s, s_rect)
                text = game_master.game.Game.FONT.render(f"{self.boss.h_n}/{self.boss.attribute_now.health}", True, (0, 0, 0))
                pygame.display.get_surface().blit(text, text.get_rect(center=s_rect.center))
        self.player.bag.render_inventory()
        self.__ui_state.render(self.player)
        if self.player.bag.state:
            self.player.bag.render()
        elif self.player.sys_state:
            self.player.sys_state.render()

    def render(self, dt):
        if not self.__item.state:
            self.__item.state = 1
        if self.boss_map:
            self.boss_camera.custom_draw(self.player.rect.copy(), dt)
        else:
            self.camera.custom_draw(self.player.rect.copy(), dt)
        self.render_UI()
        if self.__stop:
            if self.__item.d:
                self.__item.render_dead()
            else:
                self.__item.render()


class Item:
    def __init__(self, player):
        self.player = player
        self.state = 1
        self.d = 0
        self.boss = 0
        self.display = pygame.display.get_surface()
        self.b1 = pygame.Surface((100, 50))
        self.b2 = pygame.Surface((100, 50))
        self.start_frame_rect = self.b1.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        self.end_frame_rect = self.b2.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 120))
        self.start = game_master.game.Game.FONT.render("退出菜单", True, (0, 0, 0)).convert_alpha()
        self.end = game_master.game.Game.FONT.render("回到主菜单", True, (0, 0, 0)).convert_alpha()
        self.start_rect = self.start.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2))
        self.end_rect = self.end.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 120))

    def action(self, pos):
        if not self.d:
            if -self.b1.width // 2 < pos[0] - settings.WIDTH // 2 < self.b1.width // 2 and -self.b1.height // 2 < pos[1] - settings.HEIGHT // 2 < self.b1.height // 2:
                return 0
            elif -self.b2.width // 2 < pos[0] - settings.WIDTH // 2 < self.b2.width // 2 and -self.b2.height // 2 < pos[1] - settings.HEIGHT // 2 - 120 < self.b2.height // 2:
                self.state = 0
                return 1
            return 1
        else:
            if -self.b2.width // 2 < pos[0] - settings.WIDTH // 2 < self.b2.width // 2 and -self.b2.height // 2 < pos[1] - settings.HEIGHT // 2 - 60 < self.b2.height // 2:
                self.d = 0
                if self.boss:
                    t = self.player.boss_spawn_point.copy()
                    self.player.attribute.rect = t
                    self.player.rect.center = t
                    self.player.hitbox.center = t
                else:
                    t = self.player.spawn_point.copy()
                    self.player.attribute.rect = t
                    self.player.rect.center = t
                    self.player.hitbox.center = t
                self.player.h_n = self.player.attribute_now.health
                self.player.s_n = self.player.attribute_now.shield
                self.player.vec2 = [0, 0]
                self.player.move_state = "stand_back"
                return 0
            return 1

    def render_dead(self):
        b3 = self.b1.copy()
        b3.fill((255, 255, 255))
        font = game_master.game.Game.FONT.render("重生", True, (0, 0, 0)).convert_alpha()
        rect = b3.get_rect(center=(settings.WIDTH // 2, settings.HEIGHT // 2 + 60))
        self.display.blit(b3, rect)
        rect = font.get_rect(center=rect.center)
        self.display.blit(font, rect)

    def render(self):
        self.b1.fill((255, 255, 255))
        self.b2.fill((255, 255, 255))
        self.display.blit(self.b1, self.start_frame_rect)
        self.display.blit(self.b2, self.end_frame_rect)
        self.display.blit(self.start, self.start_rect)
        self.display.blit(self.end, self.end_rect)