from distutils.core import setup
setup(
  name='markdown_qrcode',
  version='0.1.1',
  maintainer="Airtonix",
  maintainer_email="airtonix@gmail.com",
  url="airtonix.net/projects/markdown-qrcode",
  py_modules=[
    'mdx_qrcode',
    'mdx_qrcode.QrCodeImageWriter',
    'mdx_qrcode.QrCodeLib',
  ],
  license='LICENSE.txt',
  description='Useful towel-related stuff.',
  long_description=open('README.txt').read(),
)

