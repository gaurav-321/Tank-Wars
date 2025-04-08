# Tank Wars 🎮

Tank Wars is an exciting multiplayer tank battle game developed using the Pygame library. The game features dynamic gameplay with player interactions, AI opponents, destructible cells, and collectible power-ups.

## ✨ Description

Tank Wars challenges players to control their tanks through a grid-based battlefield. Compete against other players or an AI opponent in real-time battles. Destroy enemy tanks, collect power-ups for temporary advantages, and navigate through the battlefield with strategic planning.

## 🚀 Features

- **Multiplayer Mode**: Play against other human players.
- **AI Opponent**: Challenge yourself against a smart AI.
- **Destructible Cells**: Destroy obstacles to progress in the game.
- **Power-Ups**: Collect power-ups for temporary benefits.
- **Dynamic Gameplay**: Engaging and responsive gameplay with sound effects.

## 🛠️ Installation

1. Clone this repository:
   ```sh
   git clone https://github.com/gag3301v/Tank-Wars.git
   ```

2. Navigate to the project directory:
   ```sh
   cd Tank-Wars
   ```

3. Install dependencies using pip:
   ```sh
   pip install pygame
   ```

## 📦 Usage

### Running the Game

To start the game, run `main_file.py`:
```sh
python main_file.py
```

This will open a Pygame window with a menu where you can select to play against another player or an AI opponent.

### Input Handling

- **Player Controls**: Use mouse clicks to move your tank around the grid.
- **Quit Game**: Click the close button in the game window to exit.

## 🎮 Gameplay Mechanics

1. **Grid Movement**:
   - Both tanks can move, but they cannot move through deactivated robots or off the grid.

2. **Health System**:
   - Each tank starts with a certain health. Colliding with an deactivated robot decreases its health.
   - Health reaches zero when a tank is destroyed.

3. **Collision Detection**:
   - The game checks for collisions and handles them appropriately, removing tanks from the game when necessary.

4. **Sound Effects**:
   - Simple sound effects enhance the gaming experience, including clicks, destruction, and start of the game.

## 🚀 Improvements and Considerations

1. **Enhanced Movement Logic**:
   - Implement more complex pathfinding algorithms for better AI behavior.

2. **User Interface**:
   - Add a user interface to display scores, health bars, and other relevant information.

3. **Graphics**:
   - Improve the graphics by adding more detailed images for tanks, deactivated robots, and lasers.

4. **AI Behavior**:
   - Enhance the AI's behavior by making it smarter in choosing its moves (e.g., avoiding obstacles, moving towards the player).

5. **Sound Effects**:
   - Add more sound effects to enhance the gaming experience.

6. **Error Handling**:
   - Implement error handling to ensure smooth gameplay without crashes due to unexpected inputs or conditions.

## 🌐 Contributing

Contributions are welcome! Feel free to fork this repository and submit a pull request with your improvements.

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

Enjoy playing Tank Wars! 🎮