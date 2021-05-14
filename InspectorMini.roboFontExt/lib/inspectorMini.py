# -*- coding: UTF-8 -*-

"""
A basic version of the Inspector.
Glyph | Width | Unicode

"""

#import vanilla
from vanilla import *
from mojo.events import addObserver, removeObserver
from defconAppKit.windows.baseWindow import BaseWindowController
from mojo.UI import OpenGlyphWindow


class inspectorMini(BaseWindowController):

	def __init__(self):

		# layout
		self.windowWidth = 240
		self.windowHeight = 80
		self.windowHeightMax = self.windowHeight * 3.75


		# # # # #
		# Window
		# # # # #


		self.w = FloatingWindow((self.windowWidth, self.windowHeight), "inspectorMini", minSize=(self.windowWidth, self.windowHeight), maxSize=(300, self.windowHeightMax))

		self.w.info = List((10, 10, -10, -28),
					 [],
					 columnDescriptions=[{"title": "Name", "editable":True}, {"title": "Width", "editable":True}, {"title": "Unicode", "editable":True}],
					 doubleClickCallback = self.selectGlyph,
					 )
		self.w.clear = Button((10, -24, -10, 20), "clear", callback=self.clear)

		# GO!
		self.setUpBaseWindowBehavior()
		self.w.open()
		self.run()


	# # # # # # # # #
	#  FUNCTIONS
	# # # # # # # # #


	def run(self):
		addObserver(self, "setInfo", "currentGlyphChanged")
		self.setInfo("hello")

	def windowCloseCallback(self, sender):
		removeObserver(self, "currentGlyphChanged")
		super(inspectorMini, self).windowCloseCallback(sender)


	def clear(self, sender):
		self.w.info.set([])
		self.w.resize(self.w.getPosSize()[2], self.windowHeight)
		#self.setInfo(sender)


	def uniName(self, sender, uniValue):
		return '%s' % (format((uniValue), 'x').zfill(4).upper())


	def setInfo(self, sender):
		l = self.w.info.get()
		
		if CurrentFont() != None:

			if CurrentGlyph() != None:
				g = ({"Name": CurrentGlyph().name, "Width": CurrentGlyph().width, "Unicode": ', '.join(map(str, [self.uniName(sender, x) for x in CurrentGlyph().unicodes]))})
				if g in l:
					l.remove(g)
				l.append(g)
			else:
				for i in CurrentFont().selectedGlyphNames:
					uni = [str(self.uniName(sender, x)) for x in CurrentFont()[i].unicodes]
					g = ({"Name": i, "Width": CurrentFont()[i].width, "Unicode": ", ".join(uni)})
					if g in l:
						l.remove(g)
					l.append(g)
			self.w.info.set(l)

			newHeight = self.windowHeight + (len(l)*18)
			if newHeight > self.windowHeightMax:
				newHeight = self.windowHeightMax
			self.w.resize(self.w.getPosSize()[2], newHeight)

			self.w.info.setSelection([len(l)-1])
			self.w.info.scrollToSelection()


	def selectGlyph(self, sender):
		g = self.w.info.get()
		if self.w.info.getSelection() != []:
			gs = self.w.info.getSelection()[0]
			if CurrentFont() != None:
				OpenGlyphWindow(CurrentFont()[g[gs]["Name"]], newWindow=False)


if __name__ == "__main__":
	inspectorMini()
