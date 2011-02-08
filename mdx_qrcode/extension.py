#!/usr/bin/env python

"""
QRcode markdown filter
========================

- Copyright (c) 2011 Zenobius Jiricek
		- Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

## Format

[{First encoded data}]

[{ Second encoded data }]

[{ {Third encoded data} }]
"""


import markdown
import cStringIO
from QrCodeLib import *
from markdown import etree
from base64 import b64encode

class QrCodeExtension(markdown.Extension):
	""" QRcode Extension for Python-Markdown. """
	def __init__(self, configs):
		"""
		Create an instance of QrCodeExtension

		Keyword arguments:
		* configs: A dict of configuration settings passed in by the user.
		"""
		# Set extension defaults
		self.config = {
			'intPixelSize'  : (  2, 'Pixel Size of each dark and light bit' ),
			'intCanvasSize' : ( 10, 'Canvas Size of the QRCode' ),
		}
		# Override defaults with user settings
		for key, value in configs:
			self.setConfig(key, value)

	def add_inline(self, md, name, pattern_class, pattern):
		"""
		Add new functionality to the Markdown instance.

		Keyword arguments:
		* md: The Markdown instance.
		* md_globals: markdown's global variables.
		"""
		objPattern = pattern_class(pattern, self.config)
		objPattern.md = md
		objPattern.ext = self
		md.inlinePatterns.add(name, objPattern, '_begin')

	def extendMarkdown(self, md, md_globals):
		self.add_inline(md, 'qrcode', BasicQrCodePattern, r'\[\{\s(?P<data>.*)\s\}\]')

class BasicQrCodePattern(markdown.inlinepatterns.ImagePattern):
	def handleMatch(self, match):

		if match :
			pixel_size = 2
			qrcodeSourceData = match.group('data')
			print "--> %s" % qrcodeSourceData

			qrCodeObject = QRCode(pixel_size, QRErrorCorrectLevel.L)
			qrCodeObject.addData( qrcodeSourceData )
			qrCodeObject.make()
			qrCodeImage = qrCodeObject.makeImage(
				pixel_size = pixel_size,
				dark_colour = '#000000'
			)
			qrCodeImage_File = cStringIO.StringIO()
			qrCodeImage.save(qrCodeImage_File , format= 'PNG')
			etree = markdown.etree
			container = etree.Element('div')
			element = etree.SubElement(container, 'img')
			element.set('src', 'data:image/png;base64,%s' % b64encode( qrCodeImage_File.getvalue() ) )
			qrCodeImage_File.close()

			return element

		else :
			return None

def makeExtension(configs=None):
	return QrCodeExtension(configs=configs)

if __name__ == '__main__':
		import doctest
		print doctest.testmod()
		print '-' * 8
		print markdown.markdown(__doc__, ['qrcode'])

