# TODO

Text input
- allow aligning of the text

Chunks
- generate the whole world at once
- add a loading screen for when the world is generating
- split the world into chunks
- look at the player position and look at what chunks to render

World generation
- add coordinates to each block and include the coordinates in the generation of random noise
- add multiple layers to the world including biomes

Infinite world:
- include block coordinates in the random noise generation
- generate n+1 layers of blocks outside the chunk
- smooth the chunk (including outer layers) n times
- then shave off the outer layers of the chunk
