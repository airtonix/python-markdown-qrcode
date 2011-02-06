#!/usr/bin/env python

import os
import Image
import hashlib


from PyQRNative import *

def QrCodeImageWriter(static_root, value, pixel_size=2):
  QRCODESPATH = os.path.join(static_root, "qrcode")
  if not os.path.exists( QRCODESPATH ):
    os.makedirs(QRCODESPATH)

  query_hash = hashlib.md5()
  query_hash.update( value )
  md5 = query_hash.hexdigest()

  filename = "%s.png" % md5
  filepath = os.path.join(QRCODESPATH, filename)

  if not os.path.exists( filepath ) :
    qrCodeObject = QRCode(pixel_size, QRErrorCorrectLevel.L)
    qrCodeObject.addData( value )
    qrCodeObject.make()
    qrCodeImage = qrCodeObject.makeImage(
      pixel_size = pixel_size,
      dark_colour = "#000000"
    )
    qrCodeImage.save( filepath )

  return filepath

