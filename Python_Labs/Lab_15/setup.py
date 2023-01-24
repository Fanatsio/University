from distutils.core import setup, Extension
my_module = Extension('_my', sources=['my_wrap.c', 'my.c'])
setup(
    name = 'my',
    ext_modules = [my_module],
    py_modules = ["my"]
)
#python3 setup.py build_ext --inplace 
