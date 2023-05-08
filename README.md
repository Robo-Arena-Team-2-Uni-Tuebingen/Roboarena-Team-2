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
  - `TileHeight` and `TileWidth` define the size of the single tiles
  - `ArenaHeight` and `ArenaWidth` define the number of tiles
- the layout of the arena get saved in a matrix which is randomly filled at the beginning
  - the integers 0-5 represent the different tile types
  
 ![draw-tiles](https://user-images.githubusercontent.com/83218599/236783524-cb39afd0-7526-4da4-9bc3-08d22aa5d660.png)
- `paintEvent` goes through the entrys of the matrix and `drawTile` paints the single tiles
- color of the tiles is defined by the array `colorTable` (integer in the matrix ArenaLayout is index in colorTable)

![widget-with-arena](https://user-images.githubusercontent.com/83218599/236785209-5d0fb1ae-c55a-47c8-bbd9-6c9795df245e.png)
- the arena is a widget on the main window which is centered

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
<img width="634" alt="Bildschirmfoto 2023-05-08 um 10 41 44" src="https://user-images.githubusercontent.com/104011823/236791247-d3db714b-108c-49e9-8f9e-d4b31e21d7aa.png">

