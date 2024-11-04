from camera import Camera
from settings import *
import pygame as pg


"""
	Handles keyboard and mouse events
"""
class Player(Camera):
	def __init__(self, app, position=PLAYER_POS, yaw=-90, pitch=0):
		self.app = app
		super().__init__(position, yaw, pitch)


	def update(self):
		self.keyboard_control()
		self.mouse_control()
		super().update()


	def handle_event(self, event):
		# voxel interaction using mouse clicks
		if event.type == pg.MOUSEBUTTONDOWN:
			voxel_handler = self.app.scene.world.voxel_handler
			if event.button == 1:
				voxel_handler.set_voxel()
			if event.button == 3:
				voxel_handler.switch_mode()


	def mouse_control(self):
		mouse_dx, mouse_dy = pg.mouse.get_rel()

		# wraps mouse around if at edges
		mouse_x, mouse_y = pg.mouse.get_pos()
		x, y = mouse_x, mouse_y

		if mouse_x == 0:
			x = WIN_RES[0]
		elif mouse_x == WIN_RES[0] - 1:
			x = 0
		elif mouse_y == 0:
			y = WIN_RES[1]
		elif mouse_y == WIN_RES[1] - 1:
			y = 0
			
		if x == 0 or x == WIN_RES[0] or y == 0 or y == WIN_RES[1]:
			mouse_dx, mouse_dy = 0, 0

		pg.mouse.set_pos(x, y)

		if mouse_dx:
			self.rotate_yaw(delta_x=mouse_dx * MOUSE_SENSITIVITY)
		if mouse_dy:
			self.rotate_pitch(delta_y=mouse_dy * MOUSE_SENSITIVITY)


	def keyboard_control(self):
		key_state = pg.key.get_pressed()
		vel = PLAYER_SPEED * self.app.delta_time

		if key_state[pg.K_w]:
			self.move_forward(vel)
		if key_state[pg.K_s]:
			self.move_back(vel)
		if key_state[pg.K_d]:
			self.move_right(vel)
		if key_state[pg.K_a]:
			self.move_left(vel)
		if key_state[pg.K_q]:
			self.move_up(vel)
		if key_state[pg.K_e]:
			self.move_down(vel)


