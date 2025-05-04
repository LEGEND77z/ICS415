Project 3: Minecraft-like Game Engine
Project Overview
This project is a simplified Minecraft-like engine implemented using Java and LWJGL (Lightweight Java Game Library). It demonstrates foundational concepts of 3D computer graphics, including rendering textured 3D blocks, basic camera controls, and interactive world-building features such as block placement and removal.

Features
3D Block Rendering: Renders textured cubes forming a basic voxel-based world.

Texture Mapping: Applies textures from a texture atlas to each face of the cubes for realistic visuals.

Interactive Camera: Implements a first-person camera with WASD movement and mouse-driven rotation.

Block Manipulation: Allows placing and destroying blocks interactively with mouse inputs (left-click to destroy, right-click to place).

Raycasting: Precisely identifies which block the user is interacting with, enabling accurate manipulation.

Technologies Used
Java: Programming language used for development.

LWJGL: Graphics library that provides OpenGL bindings for Java.

GLFW: Library utilized for handling window management and user input.

JOML: Math library for linear algebra, matrices, and vectors operations.

GLSL Shaders: Custom vertex and fragment shaders for rendering textures.

Getting Started
Follow these instructions to run the project on your local machine:

Prerequisites
Java Development Kit (JDK) version 17 or later. (Download JDK)

LWJGL 3.3.3 or later (Download LWJGL)

IntelliJ IDEA (recommended) or any preferred IDE for Java development (Download IntelliJ)

Installation
Clone the Repository:
bash
نسخ
تحرير
git clone https://github.com/yourusername/computer-graphics-projects.git
cd computer-graphics-projects/Project3-MinecraftLikeEngine
Setting up the Project in IntelliJ IDEA:
Open IntelliJ IDEA and select "File → Open...", then choose the Project3 directory.

Navigate to "File → Project Structure...".

Go to "Libraries", click "+", select "Java", and add LWJGL jars downloaded from the official website.

Include native LWJGL libraries for your OS (Windows, Linux, macOS).

Project Structure
css
نسخ
تحرير
Project3-MinecraftLikeEngine/
├── src/
│   ├── shaders/
│   │   ├── vertexShader.glsl
│   │   └── fragmentShader.glsl
│   ├── textures/
│   │   └── block_atlas.png
│   ├── Block.java
│   ├── Camera.java
│   ├── World.java
│   ├── ShaderUtils.java
│   ├── TextureUtils.java
│   ├── Raycaster.java
│   └── BlockStorm.java
└── README.md
Running the Application
Run the BlockStorm class (the entry point).

Controls:

Move: W A S D

Look: Move mouse

Place Block: Right mouse button

Destroy Block: Left mouse button

Troubleshooting Common Issues
Textures not loading properly?

Ensure textures/block_atlas.png is in the correct path (src/textures).

Verify texture coordinates (UV mapping) if textures appear distorted.

Blocks placing incorrectly?

Adjust raycasting precision or check vector math within the Raycaster class.

License
This project is licensed under the MIT License—see the LICENSE file for details.

Acknowledgments
Inspired by Minecraft by Mojang Studios.

LWJGL documentation: LWJGL Official Docs

JOML documentation: JOML Github

Enjoy building your voxel worlds!
