#!/usr/bin/env python

"""
QRcode markdown filter
========================

- Copyright (c) 2011 Zenobius Jiricek
    - Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php


format

    [intPixelSize#strDataToEncode]

ie :
    [2#555-35432]

or without pixel size
    [2#555-35432]

returns
    <img src="data:image/png;base64,blahblahblah" title="555-35432"/>
"""

import StringIO

from QrCodeLib import *
import markdown, re
from markdown import etree
from base64 import b64encode

PATTERN_QRCODE = r"""\[(?P<intPixelSize>[\d]*)#(?P<strDataToEncode>[^*]+)\]"""
REGEX_QRCODE = re.compile( PATTERN_QRCODE )
PATTERN_TEST_QRCODE = r""".*"""

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
          "intPixelSize" : [
            2,
            "Pixel Size of each dark and light bit"
          ],
          "intCanvasSize" : [
            10,
            "Canvas Size of the QRCode"
          ],

        }

        # Override defaults with user settings
        for key, value in configs:
            self.setConfig(key, value)


    def extendMarkdown(self, md, md_globals):
        """
        Add new functionality to the Markdown instance.

        Keyword arguments:
        * md: The Markdown instance.
        * md_globals: markdown's global variables.

        """
        self.md = md

        # append to end of inline patterns

        qrcodePattern = QrCodePattern(PATTERN_QRCODE, self.config)
        qrcodePattern.md = md
        md.inlinePatterns.add('qrcode', qrcodePattern, "<not_strong")



class QrCodePattern(markdown.inlinepatterns.Pattern):
  RE = re.compile(PATTERN_QRCODE)

  def __init__(self, pattern, config):
    markdown.inlinepatterns.Pattern.__init__(self, pattern)
    self.config = config

  def test(self, parent, block):
    return bool(self.RE.search(block))

    def handleMatch(self, match):
        if match.group("strDataToEncode").strip():
          return self.renderImageTag( match.group("strDataToEncode").strip() )
        else :
          return ""

  def renderImageTag(self, match = None):
    if match :
      qrcodeSourceData = match.group('strDataToEncode')
      qrcodePixelSize = match.group('intPixelSize')

      if not qrcodePixelSize :
        qrcodePixelSize = self.getConfig("intPixelSize")

      element = markdown.etree.Element('img')
      element.set("src", make_image(qrcodeSourceData, qrcodePixelSize ) )
      element.set("title", qrcodeSourceData )

      return element

def make_image(data, pixel_size):

  qrCodeObject = QRCode(pixel_size, QRErrorCorrectLevel.L)
  qrCodeObject.addData( data )
  qrCodeObject.make()
  qrCodeImage = qrCodeObject.makeImage(
    pixel_size = pixel_size,
    dark_colour = "#000000"
  )

  qrCodeImage_File = StringIO.StringIO()
  qrCodeImage.save( qrCodeImage_File , format= 'PNG')
  output ="data:image/png;base64,%s" % b64encode( qrCodeImage_File.getvalue() )
  qrCodeImage_File.close()

  return output


def makeExtension(configs=None):
    return QrCodeExtension(configs=configs)

if __name__ == "__main__":
    import doctest
    doctest.testmod()
    print "<img src='%s' />" % make_image("test", 2)

