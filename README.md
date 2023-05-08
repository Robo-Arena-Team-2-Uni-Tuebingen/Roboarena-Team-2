# Roboarena-Team-2
## Sprints
### Sprint 1 (04.04. - 24.04.2023)
- Created the Roboarena-Team-2 repository
- Set up the [GitHup.io page](https://robo-arena-team-2-uni-tuebingen.github.io/Roboarena-Team-2/)
- Added a workflow with a Flake8 test which checks the syntax of uploaded Python code
- Created and tested the first programms and pushed them to the repository. All passed the Flake8 test

### Sprint 2 (26.04. - 09.05.2023)
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

#### Robot (by Julian Häberle)

- implemented all the required attributes (x, y, radius, alpha)
- minor problems with the alpha attribute, currently it doesn’t correctly respond to a input in degrees and requires an input as a fraction of pi instead, fix for that will come with the next sprint
-  minor problems with the flipped y-axis of the drawing, took a while to figure out
- implemented a getAlpha method that is supposed to calculate the angle (relative to the x-axis) to any given point in preparation for a possible mouse-control scheme, currently untested though
- ![grafik](https://user-images.githubusercontent.com/67464857/236786215-f5586590-0c8e-4e42-89b9-f123d0026a9f.png)
