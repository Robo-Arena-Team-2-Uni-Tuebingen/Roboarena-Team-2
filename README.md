# Roboarena-Team-2
## Sprints
### Sprint 1 (04.04. - 24.04.2023)
- Created the Roboarena-Team-2 repository
- Set up the [GitHup.io page](https://robo-arena-team-2-uni-tuebingen.github.io/Roboarena-Team-2/)
- Added a workflow with a Flake8 test which checks the syntax of uploaded Python code
- Created and tested the first programms and pushed them to the repository. All passed the Flake8 test

### Sprint 2 (26.04. - 09.05.2023)

#### Repository update
- changed repository to organization repo to give equal admin rights
- setting up Kanban for future sprints

#### Wireframe
![wireframe](https://user-images.githubusercontent.com/83218599/236781331-fe7f95dc-c2bc-4c22-b083-839dffdfba7d.png)

#### Arena class (by Niklas Wolf)
![arena-class](https://user-images.githubusercontent.com/83218599/236781672-8ad60e9a-917e-40a3-bf30-762b0ba8af87.png)
- the size of the arena are set at the beginning of the class
  - `TileHeight` and `TileWidth` define the size of the single tiles in pixels
  - `ArenaHeight` and `ArenaWidth` define the number of tiles
- the layout of the arena get saved in a matrix which is randomly filled at the beginning
  - the integers 0-5 represent the different tile types
  
 ![draw-tiles](https://user-images.githubusercontent.com/83218599/236783524-cb39afd0-7526-4da4-9bc3-08d22aa5d660.png)
- `paintEvent` iterates through the entrys of the matrix and calls `drawTile` which paints the single tiles
- color of the tiles is defined by the array `colorTable` (integer in the matrix ArenaLayout is index in colorTable)

![widget-with-arena](https://user-images.githubusercontent.com/83218599/236785209-5d0fb1ae-c55a-47c8-bbd9-6c9795df245e.png)
- the main window creates an arena as a widget

![random-arena](https://user-images.githubusercontent.com/83218599/236785494-0a48e9a5-9df2-439c-81fb-60163cee000c.png)
- result of a random arena layout

#### Arena Refactor (by Julian Häberle)

- implemented ability to manipulate single tiles
- implemented ability to assign more attributes to tiles
- reason for this was mostly to lay a foundation for longterm considerations

![grafik](https://user-images.githubusercontent.com/67464857/236786951-a1109422-72d1-4d12-86dc-e6f7375b466d.png)
- refactored `initArena`

![grafik](https://user-images.githubusercontent.com/67464857/236787104-4b581091-6326-45cd-9f74-acc15093371f.png)
- refactored `paintEvent` + `drawTile`

![grafik](https://user-images.githubusercontent.com/67464857/236787439-1d5b2065-1105-4737-862a-ed426ed09a99.png)
- new tiles class, which consists of a tile superclass and six tile subclasses

#### Robot (by Julian Häberle)

![grafik](https://user-images.githubusercontent.com/67464857/236787607-9fd22dec-1424-468d-88fe-359871806ce0.png)
- newly added `robot` class
- implemented all the required attributes (x, y, radius, alpha)
- minor problems with the alpha attribute, currently it doesn’t correctly respond to a input in degrees and requires an input as a fraction of pi instead, fix for that will come with the next sprint
- implemented a getAlpha method that is supposed to calculate the angle (relative to the x-axis) to any given point in preparation for a possible mouse-control scheme, currently untested though

![grafik](https://user-images.githubusercontent.com/67464857/236787884-939f4066-282c-4cdc-90a1-aa2ec010bda1.png)
- newly added method `drawRobot`, which is called from `paintEvent`
- calculates the point indicated by the angle and radius and then draws a line between it and the center of the robot
- minor problems with the flipped y-axis of the drawing, took a while to figure out, the solution was to flip the y-component of the calculation
- color orange to differentiate a bit from the tiles

![grafik](https://user-images.githubusercontent.com/67464857/236786215-f5586590-0c8e-4e42-89b9-f123d0026a9f.png)
- result of `drawRobot`

#### Movement (by Tom Kuehnle)
 - Creating timer using `QBasicTimer`
 - Setting time interval for movement ticks
<img width="627" alt="Bildschirmfoto 2023-05-08 um 10 41 35" src="https://user-images.githubusercontent.com/104011823/236791094-2d23c1c6-08fa-4b71-b69b-3700b3a2495b.png">

 - Creating `timerEvent`
 - Center of the robot moves on tiles
 - random selection of the directions up/down/left/right
 - using `TileLength` `TileWidth` and size of the arena to determine new robot position

<img width="634" alt="Bildschirmfoto 2023-05-08 um 10 41 44" src="https://user-images.githubusercontent.com/104011823/236923711-c9a7d32f-cebc-419e-a2c5-432f09112f77.png">


![Bildschirmaufnahme-2023-05-08-um-22 06 00](https://user-images.githubusercontent.com/104011823/236923814-b33b7c6a-0396-4932-879c-1d11fb63b037.gif)

### Sprint 3 (09.05.2023 - 23.05.2023)

#### Map Generator (by Julian Häberle)
- basic implementation of a randomly generated map
- uses a basic 2D simplex noise function from https://github.com/caseman/noise
- can't get it to work within the required parameters of the new tileset atm, which is why it's considered non-functional and hasn't been merged into the main yet

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/2f416593-0e6d-4fb3-a6d8-508493e1babe)

- this particular noise function always creates the same noisemap
- random factors to shift and scale the area of interest on the noisemap

Example of a generated map (with old tileset):

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/125645e1-7724-4c3b-a60a-c620e3f6be46)

#### Load map from ASCII text file (by Niklas Wolf)
![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/ae30cc9c-4638-4fe7-9ee8-2f15499946fe width=60% height=60%)
- `textToMatrix` converts a text file into a matrix of the single characters
- every line of the text file is a row in the matrix

![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/0535e3ae-ee79-445c-9ac7-d807257f3421)
- `translateAscii` compares a given character with the diffrent cases and returns the corresponding tile type
- the dafault for undefined characters is `NormalTile`

![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/87cc52f6-3c91-40ca-b103-0426b9504a46)
- `textToTiles` converts a given text file to a matrix of tiles
- `translateAscii`gets vectorized to apply it to every entry of the matrix

Example Map:
![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/0cefb76f-a642-46b1-ab60-410745133d6c)
![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/83507485-580b-4913-8799-dfddbd1370de)
- a problem with this solution is that the the text file must already have the correct dimensions of the arena

#### Graphical Tilesets and changes to the existing tileset (by Julian Häberle)
- we decided on using the Open RPG Fantasy Tileset from https://finalbossblues.itch.io/openrtp-tiles
- replaces the old tileset (Fire, Sand, Normal, Water, Ice, Wall) with a new tileset (Wall, Water, Grass, Dirt, HighGrass, Sand, Snow, Slime, Field, CobbleStone)
- this was done to implement smoother transitions and make the map look cleaner
- to accomodate for the increased tile size (16x16 vs 10x10) the size of the arena has been decreased from 100x100 to 60x60 tiles

The three mainfiles of the Open RPG Fantasy Tileset:

![dungeon](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/7950e1b6-d208-4c10-868a-346f213bfa9f)
![exterior](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/801c9fe1-9851-40a4-96ec-72393077386b)
![interior](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/af8540c2-cd2e-4538-b879-97095a522487)

Initializing and new helper functions:

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/b0c5c7ec-e92d-48ca-8b62-19a0d9a6b139)
- Images are loaded into dungeon, exterior and interior
- `getTileRect` cuts a single tile out of the bigger images
- `getBigTileRect` cuts a 3x3 tile area out of the bigger images
- tiles that do not implement a transition atm (Wall, Water, Grass (Grass is the default tile that every other tile transitions to)) only cut out a single tile
- tiles that do implement a transition cut out a big tile

Changes to the tile super class:

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/5ea6af45-0287-4bcf-a97e-f625d3a817e3)
- added an attribute `str` that contains the ascii character for the specific tile
- this was done to avoid typechecking in various situations
- the compare method uses this string to compare its own tile with another given tile

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/00b3e48f-2140-401b-bb8c-a19a96e75f9c)
- the chooseTexture method requires a list of four tiles as a parameter, the tiles above, below, left and right of the own tile
- this is a bit of a codesmell, but was done in case the function is later expanded to include all 8 context tiles
- the function then compares which of the tiles in the context is a tile of the same type
- based on that information, the appropriate tile is cut out from the big tile (which is the current texture) and assigned as the new texture of the tile
- if the tile does not match to a transition in the big tile, the standard tile is chosen
- this poses a bit of a limitation in a map design aspect as it currently requires all patches (save for patches without transitions) to be at least 2x2 (with some more limitations)

Example:

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/f45eaec9-866b-4057-84bf-f424e8f7d9e1)
- the blue marked area is the big cutout for the DirtTile
- the red cutout would be the chosen tile if the tile to the left and above would be of a different type

Tiles without implemented transition:

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/a7752a5e-8631-4c4c-bd00-906e72c80676)
- tiles without transition override the `chooseTexture` function to just return their current texture

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/30a30f80-35e8-4854-be89-b6168b694662)
- the `chooseTexture` function is executed once on every tile object in `ArenaLayout` after the layout has been generated
- corner cases are just assigned the `Tile` superclass for missing tiles to avoid null errors
- some minor changes to `robo-arena` as well as some minor changes to `ascii_layout`, but nothing noteworthy

Test map:

![grafik](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/67464857/b9c821db-5828-4fac-b0c6-3a4656015b2a)

#### Extend the robot class (by Niklas Wolf)
![image](=https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/6ce8da41-99bf-4831-a527-cc9984d99008)
- added variables that store information about the current velocity and acceleration
- at the beginning velocity and acceleration are 0 at the beginning and change with the actions of the player
- the maximum accelerations are arbitrary so far and we have to test which values make sense
  
![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/477cac12-b822-4afe-8c04-eb0ab34d017e)
- extended the `update` function to also change the speed parameters
- new accelerations get added to the old values 
- if they exceed the maximum acceleration, the maximum is taken as the acceleration value
- the new velocitys are calculated from the current velocitys and the new accelerations in relation to the time
- problem: we are not sure yet how some values should processed
  - negative velocity = robot moves backwards?
  - maximum velocity?  
![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/334d0797-8fa7-48d9-b86b-3e2c30a274a7)
- stored four robots in an array so it's easier to change the number of used robots between 1 and 4
- added the parameter color to the constructor so every robot has its indivdual color
  
![image](https://github.com/Robo-Arena-Team-2-Uni-Tuebingen/Roboarena-Team-2/assets/83218599/20294529-31dc-48a3-a23d-00511f3cd5f3)
- placed four robots on the playing field





