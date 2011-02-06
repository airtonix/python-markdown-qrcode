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

import markdown
import Image
import re
from base64 import b64encode


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

  def renderImageTag(self, match = None):
    if match :
      qrcodeSourceData = match.group('strDataToEncode')
      qrcodePixelSize = match.group('intPixelSize')

      element = markdown.etree.Element('img')
      element.set("src", self.make_image(qrcodeSourceData, qrcodePixelSize ) )
      element.set("title", qrcodeSourceData )
      return "element"

  def make_image(self, data, size):
    qrCodeObject = QRCode(pixel_size, QRErrorCorrectLevel.L)
    qrCodeObject.addData( value )
    qrCodeObject.make()
    qrCodeImage = qrCodeObject.makeImage(
      pixel_size = pixel_size,
      dark_colour = "#000000"
    )

    query_hash = hashlib.md5()
    query_hash.update( value )
    md5 = query_hash.hexdigest()

    filename = "%s.png" % md5
    filepath = os.path.join( tempfile.mkdtemp() , filename)

    qrCodeImage.save( filepath )
    qrCodeImage_File = open(filepath, "r")
    qrCodeImage_FileData = qrCodeImage_File.read()
    qrCodeImage_File.close()

    return "data:image/png;base64,%s" % b64encode( qrCodeImage_FileData )


PATTERN_QRCODE = r"""\[(?P<intPixelSize>[\d]*)#(?P<strDataToEncode>[^*]+)\]"""
REGEX_QRCODE = re.compile( PATTERN_QRCODE )
QRCODEINLINEPATTER=QrCodeInlinePattern("(.*)")

