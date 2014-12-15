from distutils.core import setup
import py2exe

setup(
    name = "Ned's Maze",
    version = "1.1",
    window = [{"script":"mazePlay.py"}],
    py_modules = ["Comp_Logo","DummyLevel","Maze_1","StartMenu"],
    data_files = [(".", ["cherry pie.jpg", "AbbeyME.ttf", "logoback.bmp", "mazeJunct1.bmp",
                         "mazeJunct2.bmp", "mazeJunct3.bmp", "mazejunct4.bmp","mazeJunct5.bmp",
                         "mazeJunct6.bmp", "mazeJunct7.bmp", "mazeJunct8.bmp","mazeJunct9.bmp",
                         "mazeJunct10.bmp", "mazeJunct11.bmp", "mazeJunct12.bmp", "mazeWall0.bmp",
                         "mazeWall1.bmp","mazeWall2.bmp","mazeWall3.bmp", "mazeWall4.bmp",
                         "mazeWall5.bmp", "mazeWall6.bmp","mazeWall7.bmp", "mazeWall8.bmp",
                         "mazeWall9.bmp","mazeWall10.bmp","mazeWall11.bmp","mazeWall12.bmp",
                         "mazeWall13.bmp","mazeWall14.bmp", "Ned.bmp","NedArrow.bmp","NedINS.bmp",
                         "NedPie.bmp","NedRed.bmp"])],
    author = "Ryan Sweeney",
    author_email = "sween119@hotmail.com",
    url = "http://mcsweenus.blogspot.com"
    )
