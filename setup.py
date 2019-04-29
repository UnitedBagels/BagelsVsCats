from cx_Freeze import setup, Executable
setup(
    name = "Bagels vs. Cats",
    version = "1.6.0",
    options = {"build_exe": {
        'packages': ["os","sys","ctypes","win32con"],
        'include_files': ['images/','android-icon.png','bagel.py','bagelsplat.ogg','bullet.py','cagedrop.ogg','cat.py','dog.py','fork.ogg','game.py','particle.py','placing.ogg','poppysplat.ogg','punch.ogg','save.dat','title.ogg','track1.ogg','visitor1.ttf','wheat.py','wizardsplat.ogg'],
        'include_msvcr': True,
    }},
    executables = [Executable("main.py",base="Win32GUI")]
    )