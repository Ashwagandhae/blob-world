# Blob world game

Blob world game is a game written in Python, using mostly [pygame](https://www.pygame.org/) and pure python. This is the first big Python project I made. Have fun!

# Usage

## Running the game

1. Make sure you have [python installed](https://www.python.org/downloads/).
2. Next, install pygame (the only dependency this project has)

```
pip3 install pygame
```

3. Finally, clone the repository and run the game

```
git clone https://github.com/Ashwagandhae/blob-world
cd blob-world
python3 blobWorldGame.py
```

## Game instructions

Here are the original instructions (you can access them in game by clicking _instructions_):

Welcome to the world of blob! Use your mouse to control where the blob in the middle goes! Avoid your enemies and knock them down with your almighty arsenal of weapons - press space to shoot, and use the arrow keys or W & S to change your weapon!

**Types of enemies:**

- Frog - hops around randomly, sometimes towards you to squash you. Doesn't have too much health.
- Squid - follows you, pulls you in with whirlpool once in a while. Has pretty high health.
- Cannon - stalks you and spams bullets towards you. Has very high health, so watch out!
- Wasps - Fly around at high speeds in swarms and sting you, but barely have any health

**Types of bullets:**

- Shooter - medium damage, medium fire rate, good knockback, no splash
- Spammer - low damage, high fire rate, medium knockback, no splash
- Sniper - very high damage, low fire rate, high knockback, no splash
- Grenader - medium-high damage, low fire rate, no knockback, big splash after a time
- Rocketier - high damage, very low fire rate, no knockback, big splash upon impact
