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

[2#555-354www32]

[[2#555-354www32]]

returns
    <img src="data:image/png;base64,blahblahblah" title="555-35432"/>
"""

test= """
[2:555-35432]

[2:http://www.somwhere.com/post/2#2]

[2:http://www.somwhere.com/post/2#2]
"""

import re
import markdown
import StringIO
from QrCodeLib import *
from markdown import etree
from base64 import b64encode

QRCODE_PATTERN_ver1 = r"""\[(?P<intPixelSize>[\w\d]*)[:](?P<strDataToEncode>[^*]+)\]"""
QRCODE_PATTERN = QRCODE_PATTERN_ver1

QRCODE_REGEX = re.compile(QRCODE_PATTERN)


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

    md.inlinePatterns.add(
      'qrcode',
      QrCodePattern(
        QRCODE_PATTERN,
        self.config
      ),
      "<reference"
    )

class QrCodePattern(markdown.inlinepatterns.Pattern):
  def __init__(self, pattern, config):
    markdown.inlinepatterns.Pattern.__init__(self, pattern)
    self.config = config

  def getCompiledRegExp(self):
    return QRCODE_REGEX

  def handleMatch(self, match):
    if match :

      qrcodeSourceData = str(match.group('strDataToEncode'))
      qrcodePixelSize = int(match.group('intPixelSize'))

      if not qrcodePixelSize :
        qrcodePixelSize = self.getConfig("intPixelSize")

      element = markdown.etree.Element('img')
      element.set("src", self.make_image( qrcodeSourceData, qrcodePixelSize ) )
      element.set("title", qrcodeSourceData )

      return element

  def make_image(self, data = "", pixel_size = 2):
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
  print markdown.markdown(test, ['qrcode'])

