import cx_Freeze

executables = [cx_Freeze.Executable("Deeper.py")]

cx_Freeze.setup(
    name = "Deeper",
    options = {"build_exe":{"packages":["pygame", "pickle"], "include_files":["toolbar.dat", "Background.png", "Bricks.png", "Clay.png", "CheckboxChecked.png", "CoalOre.png", "DeeperIcon.jpg", "DeeperIcon.ico", "dirt.png", "GoldOre.png", "grass.png", "IronOre.png", "Lamp.png", "LICENSE.txt", "mouse.png", "Mud.png", "Player.png", "PlayerSkin.png", "Stone.png", "ToolbarTile.png", "PixelFJVerdana12pt.TTF"]}},
    description = "Deeper - v0.1.2 Alpha",
    version = "0.1.2",
    executables = executables
)




































