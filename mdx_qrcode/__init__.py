#!/usr/bin/env python

"""

QRcode markdown filter,

format

 [<strDataToEncode>intPixelSize]

ie :
 [(555-35432)2]

or without pixel size
 [(555-35432)]

returns
 <img src="/tmp/qrcode/2349g09sjodg09d09fg.png" title="555-35432"/>

"""

import tempfile
import markdown
import re
from QrCodeImageWriter import *

def makeExtension(configs={}):
    return QrCodeExtension(configs=configs)

class QrCodeExtension(markdown.Extension):
    def __init__(self, configs):
        """
        Create an instance of QrCodeExtension

        Keyword arguments:
        * configs: A dict of configuration settings passed in by the user.

        """

        # Set extension defaults
        self.config = {
          "imageStoragePath" : [
            os.path.join( tempfile.mkdtemp(), "qrcode"),
            "Root path to where you want the QRcode images created"
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
        # Insert code here to add or change the behavior of Markdown.
        # Most likely instances of patterns and/or processors will be attached
        # to the Markdown instance. See the docs for more information here:
        # http://www.freewisdom.org/projects/python-markdown/Writing_Extensions

#        if 'qrcode' in md.treeprocessors.keys():
#            md.treeprocessors['qrcode'].offset += 1
#        else:
#            md.treeprocessors.add('qrcode', QrCodeProcessor(), '_end')
        md.inlinePatterns.add(
          'qrcode',
          QrCodeInlinePattern(md),
          '_begin'
        )


# Insert patterns and/or processors here.

class QrCodeInlinePattern(markdown.inlinepatterns.Pattern):
  def handleMatch(self, match):
    return self.renderImageTag(match)

  def renderImageTag(match = None):
    if match :
      qrcodeSourceData = match.group('strDataToEncode')
      qrcodePixelSize = match.group('intPixelSize')

      element = markdown.etree.Element('img')
      element.set("src", QrCodeImageWriter( self.getConfig("imageStoragePath"), qrcodeSourceData, qrcodePixelSize ) )
      element.set("title", qrcodeSourceData )
      return "element"

PATTERN_QRCODE = r"""\[(?P<intPixelSize>[\d]*)#(?P<strDataToEncode>[^*]+)\]"""
REGEX_QRCODE = re.compile( PATTERN_QRCODE )
QRCODEINLINEPATTER=QrCodeInlinePattern("(.*)")

