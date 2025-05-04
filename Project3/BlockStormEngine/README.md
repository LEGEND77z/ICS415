# Project 3: Minecraft-like Game Engine

## Overview
This project is a simplified Minecraft-like voxel engine implemented using Java and LWJGL. It provides foundational 3D graphics features, including rendering textured cubes, interactive camera movement, block placement, and destruction.

## Features
- **3D Block Rendering:** Displays textured voxel-based cubes.
- **Texture Mapping:** Applies textures from a texture atlas to blocks.
- **Interactive Camera:** WASD and mouse-driven camera navigation.
- **Block Manipulation:** Left-click to remove blocks; right-click to place blocks interactively.
- **Raycasting:** Accurately detects targeted blocks for interaction.

## Technologies Used
- **Java:** Primary programming language.
- **LWJGL:** Lightweight Java Game Library for OpenGL integration.
- **GLFW:** Handles window creation and user input.
- **JOML:** Math library for vector and matrix operations.
- **GLSL Shaders:** Custom shaders for rendering blocks.

## Getting Started

### Prerequisites
- Java Development Kit (JDK 17+)
- LWJGL 3.3.3 or later
- IntelliJ IDEA or similar IDE

### Installation & Setup
1. Clone the repository:
```bash
git clone https://github.com/yourusername/computer-graphics-projects.git
cd computer-graphics-projects/Project3-MinecraftLikeEngine
Open the project in IntelliJ IDEA:

Launch IntelliJ IDEA.

Choose File → Open... and select the Project3-MinecraftLikeEngine folder.

Configure LWJGL libraries:

Go to File → Project Structure → Libraries.

Click the + button, select Java, and add all the LWJGL .jar files you downloaded (e.g., lwjgl.jar, lwjgl-glfw.jar, etc.).

Be sure to include native libraries for your OS (e.g., lwjgl-natives-windows.jar).

Project Structure
css
نسخ
تحرير
Project3-MinecraftLikeEngine/
├── shaders/
│   ├── vertexShader.glsl
│   └── fragmentShader.glsl
├── textures/
│   └── block_atlas.png
├── src/
│   ├── BlockStorm.java       # Main class
│   ├── Block.java
│   ├── Camera.java
│   ├── World.java
│   ├── ShaderUtils.java
│   ├── TextureUtils.java
│   └── Raycaster.java
└── README.md
Controls
Move: W A S D

Look: Move mouse

Place Block: Right click

Break Block: Left click

Exit Game: Esc

