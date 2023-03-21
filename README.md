# Project-X
### Description:
This is a project i am making for a school subject.
The subject is called Java but for some reason we must now program in python.
Who cares, i got a buggy ass game

Oh yeah this game will support multiplayer over TCP/IP in the future, or for normal people, you can stick your pc in a switch, connect other pc's and play together.

### HOW TO INSTALL:
1. check if you have python 3.9 installed
if yes, proceed to step 5.
if no, go to step 2.
2. download the installer from the latest version.
3. execute the installer once it's downloaded.
4. open a command prompt and type `python --version` in it, smack that enter button.
if it says 3.9 goodjob, otherwise please remove the other python versions.
5. download the actual game from the latest release.
6. unzip the zip file
7. run the `BEFORE RUNNING.bat`
this will install the necessary libraries
8. when this is done you can open the `Project X.bat` to open the game!

### MAP MODDING:
I am a terrible map maker, so of course i made making custom maps way too difficult for the normal human.
few steps for it, i'll leave a template for it here:
```
{
    "name": "template",
    "description": "template",
    "version": "1.0",
    "objects": [
        {
            "collision": false,
            "platform": false,
            "x": 0,
            "y": 250,
            "width": 1920,
            "height": 830,
            "color": "blue"
        },
        {
            "collision": true,
            "platform": false,
            "x": 0,
            "y": 0,
            "width": 1920,
            "height": 250,
            "color": "green"
        }
    ]
}
```
This template creates a basic world with green green grass, a blue blue sky.
I'll try to explain this as much as i can:
1. we have a name, doesn't matter i use the filename in the game.
2. a description, just fill it in, might use it in the future.
3. version, i have no idea why i put it in there.
4. objects, these lil blocks get drawn from top to bottom, so the blue block first and then the green one on top.
6. collision, this is easy, is your block background? no? turn it on.
7. platform, turn it on if your block is hovering.
8. x, left bottom of your block along the left right axis
9. y, left bottom of your block along the up down axis, starts at the bottom
10. width, how big is your block from left to right.
11. height, how tall is your block.
12. color, i'll just drop the available colors here.
- grey
- aspargus
- green
- blue
- red
- yellow
- black
- white
- brown
- orange
- purple
- pink
- cyan
13. oh boy, when you have your template json, you can yeet in in `gamedirectory\Project-X\assets\levels` 
14. give it an actual name, boot the game, select your map and go into map preview, from here you can preview the map and it'll change in real time!
