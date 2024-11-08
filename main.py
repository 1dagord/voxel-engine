from shader_program import ShaderProgram
from textures import Textures
from player import Player
from scene import Scene
from settings import *
import moderngl as mgl
import pygame as pg
import sys


class VoxelEngine:
	def __init__(self):
		pg.init()

		# sets version of OpenGL
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
		pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)

		# prohibits deprecated functions
		pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)

		# sets depth buffer size
		pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

		pg.display.set_mode(WIN_RES, flags=pg.OPENGL | pg.DOUBLEBUF)
		self.ctx = mgl.create_context()

		# activates color blending, depth testing, and culling of invisible faces
		self.ctx.enable(flags=mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)

		# activates garbage collection of OpenGL objects
		self.ctx.gc_mode = "auto"

		self.clock = pg.time.Clock()
		self.delta_time = 0
		self.time = 0

		pg.event.set_grab(True)
		pg.mouse.set_visible(False)

		self.is_running = True
		self.on_init()


	def on_init(self):
		self.textures = Textures(self)
		self.player = Player(self)
		self.shader_program = ShaderProgram(self)
		self.scene = Scene(self)


	"""
		Increments time value by milliseconds
		Displays frame rate as title of window
	"""
	def update(self):
		self.player.update()
		self.shader_program.update()
		self.scene.update()

		self.delta_time = self.clock.tick()
		self.time = pg.time.get_ticks() * 0.001
		pg.display.set_caption(f"{self.clock.get_fps() :.0f}")


	"""
		Clears frame and depth buffer, then updates screen
	"""
	def render(self):
		self.ctx.clear(color=BG_COLOR)
		self.scene.render()
		pg.display.flip()


	"""
		Quits app if ESC key pressed
		Handles voxel interactions through mouse clicks
	"""
	def handle_events(self):
		for event in pg.event.get():
			if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
				self.is_running = False
			self.player.handle_event(event=event)


	def run(self):
		while self.is_running:
			self.handle_events()
			self.update()
			self.render()
		pg.quit()
		sys.exit()


if __name__ == "__main__":
	app = VoxelEngine()
	app.run()


	