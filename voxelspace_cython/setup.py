from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


exts = ('getpixel',)

#extensions = [Extension(e, ['%s.pyx' % e], extra_compile_args=['-O3']) for e in exts]
extensions = [Extension(e, ['%s.pyx' % e]) for e in exts]

setup(
    ext_modules = cythonize(extensions),
)
