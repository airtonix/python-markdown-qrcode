from distutils.core import setup
setup(
  name='markdown_qrcode',
  version='0.0.2',
  maintainer="Airtonix",
  maintainer_email="airtonix@gmail.com",
  url="airtonix.net/projects/markdown-qrcode",
  py_modules=[
    'mdx_qrcode',
    'mdx_qrcode.QrCodeLib',
  ],
  license='LICENSE.txt',
  description='A markdown extension to insert qrcode datauri images based on supplied data.',
  long_description=open('README.txt').read(),
)

