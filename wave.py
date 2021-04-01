"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

Jin Ryu jfr224
December 4th 2018
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.

    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen.
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of
    aliens.

    If you want to pause the game, tell this controller to draw, but do not update.  See
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.

    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None]
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]

    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that
    you need to access in Invaders.  Only add the getters and setters that you need for
    Invaders. You can keep everything else hidden.

    You may change any of the attributes above as you see fit. For example, may want to
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _aliensDirection: the Direction in which aliens are moving
    _alienStep: number of steps since the last Alien Bolt was fired
    _gameResult: whether the player won or not
    _alienSpeed: the number of seconds (0 < float <= 1) between alien steps
    _score: score collected when aliens have been killed
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setShip(self):
        """
        Creates the attribute _ship.
        """
        self._ship = Ship()

    def getShip(self):
        """
        Returns the attribute _ship.
        """
        return self._ship

    def setAliens(self):
        """
        Creats the attribute _aliens by looping through the table of aliens
        created. Then it sets the attributes _aliensDirection and _alienStep.
        """
        aliens = []
        for row in range(ALIEN_ROWS):
            aliens.append([])
            for col in range(ALIENS_IN_ROW):
                alien = Alien(row+1, col+1)
                aliens[row].append(alien)
        self._aliens = aliens
        self._aliensDirection = "Right"
        self._alienStep = 0

    def setBolts(self):
        """
        Creates the attribute _bolts by initializing one alien bolt.
        """
        self._bolts = []
        self.addAlienBolt()

    def addAlienBolt(self):
        """
        Adds a new alien bolt to be fired from a random alien at random time
        into the list _bolts.
        """
        firingAlien = self.whos_firing(self.randomColumn())
        when_to_fire = random.randrange(1, BOLT_RATE)

        newAlienBolt = Bolt(firingAlien, 'alien', when_to_fire)
        self._bolts.append(newAlienBolt)

    def whos_firing(self, v_aliens):
        """
        Returns the alien that will fire a bolt, after finding the lowest alien
        among the aliens from the column given.

        Parameter v_aliens: the list that contains the vertial column of aliens
        Precondition: a one-dimension list of Alien objects
        """
        for alien in range(ALIEN_ROWS):
            bottomAlien = (ALIEN_ROWS-1) - alien
            if v_aliens[bottomAlien] != None :
                return v_aliens[bottomAlien]

    def randomColumn(self):
        """
        Returns a random Column of aliens in self._aliens table.
        """
        list = [None]*ALIEN_ROWS
        while list == [None]*ALIEN_ROWS:
            col_number = random.randint(1, ALIENS_IN_ROW)
            list = []
            for row in self._aliens:
                list.append(row[col_number-1])
        return list

    def setDline(self):
        """
        Creates the attribute _dline.
        """
        points = [0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE]
        color = 'black'
        self._dline = GPath(points = points, linewidth = 1, linecolor = color)

    def getLives(self):
        """
        Returns the attribute _lives.
        """
        return self._lives

    def getResult(self):
        """
        Returns teh attribute _gameResult.
        """
        return self._gameResult

    def getScore(self):
        """
        Returns the attribute _score.
        """
        return self._score

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self, lives, alienspeed, score):
        """
        Creates ship, aliens bolts, defense line, and sets wave attributes such
        as _time, _lives, _gameResult, _alienSpeed, and _score. Other attributes
        such as _aliensDirection and _alienStep are initialized in setAliens()
        helper method.

        Parameter lives: number of lives that the player is initially given
        Precondition: an int between 1 <= lives <= SHIP_LIVES

        Parameter alienspeed: the number of seconds between alien steps
        Precondition: a float between 0 < alienspeed <= 1

        Parameter score: score collected when aliens have been killed
        Precondition: an int greater than 0
        """
        self.setShip()
        self.setAliens()
        self.setBolts()
        self.setDline()
        self._time = 0
        self._lives = lives

        self._gameResult = None
        self._alienSpeed = alienspeed
        self._score = score

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, dt, input):
        """
        Animates a single frame in the game and update the whole wave object by
        using several update methods.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)

        Parameter input: user input used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        if self._ship != None:
            self.shipMoving(input)

        self.aliensMoving(dt)

        self.update_Player_Bolt(input)

        self.update_Alien_Bolt()

        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                self.alien_collides(bolt)
            if not bolt.isPlayerBolt():
                self.ship_collides(bolt)

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws Alien, Ship, and Defense line, and Bolt objects.

        Paramter view: the game view, used in drawing
        Precondition: instance of GView; it is inherited from GameApp
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)

        if self._ship != None:
            self._ship.draw(view)

        self._dline.draw(view)

        for bolt in self._bolts:
            active = not bolt.isPlayerBolt() and bolt.getBoltState() == 'active'
            active_alienBolt = active
            if bolt.isPlayerBolt() or active_alienBolt:
               bolt.draw(view)

    # HELPER METHODS FOR COLLISION DETECTION
    def shipMoving(self, input):
        """
        Helper function for update method that updates the ship's position.

        Parameter input: user input used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        da = 0
        if input.is_key_down('right'):
            da += SHIP_MOVEMENT
        if input.is_key_down('left'):
            da -= SHIP_MOVEMENT

        if (self._ship.x + da) < (SHIP_WIDTH/2):
            self._ship.x = SHIP_WIDTH/2
        elif (self._ship.x + da) > (GAME_WIDTH - SHIP_WIDTH/2):
            self._ship.x = (GAME_WIDTH - SHIP_WIDTH/2)
        else:
            self._ship.x += da

    def aliensMoving(self, dt):
        """
        Helper function for update method that updates the aliens' positions.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._time += dt
        if self._time >= self._alienSpeed:
            if self._aliensDirection == "Right":
                self.MovingRight()
            elif self._aliensDirection == "Left":
                self.MovingLeft()
            self._time -= self._alienSpeed
            self._alienStep += 1

    def MovingRight(self):
        """
        Helper function for aliensMoving() when aliens are moving to the right
        side. First finds the rightmost alien inside _aliens table and see if
        it should move down and turn left. If it does not have to, then all the
        aliens walk to the right by one step.
        """
        rightmost_alien = self.find_rightmostA()

        max_X = GAME_WIDTH - ALIEN_H_SEP - ALIEN_WIDTH/2
        if rightmost_alien.x >= max_X:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.y -= ALIEN_V_WALK
                        self._aliensDirection = "Left"
        else:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.x += ALIEN_H_WALK

    def find_rightmostA(self):
        """
        Find the rightmost alien among the aliens from self._aliens.
        """
        all_x = [0]
        rightmost_alien_row = 0
        rightmost_alien_col = 0
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if self._aliens[row][col] != None:
                    if self._aliens[row][col].x > max(all_x):
                        rightmost_alien_row = row
                        rightmost_alien_col = col
                    all_x += [self._aliens[row][col].x]

        all_x.remove(0)
        rightmost_alien= self._aliens[rightmost_alien_row][rightmost_alien_col]
        return rightmost_alien

    def MovingLeft(self):
        """
        Helper function for aliensMoving() when aliens are moving to the left
        side. First finds the leftmost alien inside _aliens table and see if
        it should move down and turn right. If it does not have to, then all the
        aliens walk to the left by one step.
        """
        leftmost_alien = self.find_leftmostA()

        min_X = ALIEN_H_SEP + ALIEN_WIDTH/2
        if leftmost_alien.x <= min_X:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.y -= ALIEN_V_WALK
                        self._aliensDirection = "Right"
        else:
            for row in self._aliens:
                for alien in row:
                    if alien != None:
                        alien.x -= ALIEN_H_WALK

    def find_leftmostA(self):
        """
        Find the leftmost alien among the aliens from self._aliens.
        """
        all_x = [GAME_WIDTH]
        leftmost_alien_row = 0
        leftmost_alien_col = 0
        for row in range(len(self._aliens)):
            for col in range(len(self._aliens[row])):
                if self._aliens[row][col] != None:
                    if self._aliens[row][col].x < min(all_x):
                        leftmost_alien_row = row
                        leftmost_alien_col = col
                    all_x += [self._aliens[row][col].x]

        all_x.remove(GAME_WIDTH)
        leftmost_alien = self._aliens[leftmost_alien_row][leftmost_alien_col]
        return leftmost_alien

    def update_Player_Bolt(self, input):
        """
        Creates and updates the upward motion of a player bolt. While there is
        no player bolt being fired on the screen, if the player presses spacebar
        from keyboard, the ship fires a player bolt. If the bolt reaches the
        top of the screen, the bolt disappears.

        Parameter input: the user input, used to control the ship and change state
        Precondition: instance of GInput; it is inherited from GameApp
        """
        if not self.player_bolt_on_screen():
            if self._ship != None and input.is_key_down('spacebar'):
                    self._bolts.append(Bolt(self._ship, 'ship'))
        else:
            for bolt in self._bolts:
                if bolt.isPlayerBolt():
                    bolt.y += BOLT_SPEED
                    if bolt.y >= GAME_HEIGHT + BOLT_HEIGHT/2:
                        self._bolts.remove(bolt)

    def player_bolt_on_screen(self):
        """
        Helper function for update method that returns True/False if there is
        a player bolt active and on the screen.
        """
        for bolt in self._bolts:
            if bolt.isPlayerBolt():
                return True
        return False

    def update_Alien_Bolt(self):
        """
        Creates and updates the downward motion of alien bolts. If the
        designated amount of alien steps have passed, state of the alien bolt
        becomes active and is fired downwards. After being fired, the bolt's x
        position does not have to follow that of the alien. If the bolt reaches
        the bottom of the screen, the bolt disappears.
        """
        if self._alienStep == self.steps_to_be_passed():
            for bolt in self._bolts:
                if not bolt.isPlayerBolt() and bolt.getBoltState()=='inactive':
                    step = bolt.getWhenToFire()
                    bolt.setBoltState('active')
            self._alienStep -= step
            self.addAlienBolt()
        for bolt in self._bolts:
            if not bolt.isPlayerBolt():
                if bolt.getBoltState() == 'inactive':
                    alien = bolt.getWhichAlien()
                    bolt.x = alien.x
                if bolt.getBoltState() == 'active':
                    bolt.y -= BOLT_SPEED
                    if bolt.y + BOLT_HEIGHT/2 <= 0:
                        self._bolts.remove(bolt)

    def steps_to_be_passed(self):
        """
        Helper function for update_Alien_Bolt; returns amount of alien steps
        to be passed in order to fire the alien bolt.
        """
        steps = 0

        for bolt in self._bolts:
            if not bolt.isPlayerBolt() and bolt.getBoltState() == 'inactive':
                steps = bolt.getWhenToFire()
                return steps

    def alien_collides(self, bolt):
        """
        Check all the aliens in the list if each collides with this specific
        bolt. If it does, then the alien becomes None.

        Parameter bolt: the bolt that is tested if it collides with any alien
        Precondition: a player bolt from the Bolt class
        """
        for row in range(ALIEN_ROWS):
             for alien in range(ALIENS_IN_ROW):
                 if self._aliens[row][alien] != None:
                     if self._aliens[row][alien].collides(bolt):
                         self._aliens[row][alien] = None
                         self._bolts.remove(bolt)
                         self._score += 20
                         self._alienSpeed *= 0.97

    def ship_collides(self, bolt):
        """
        Check the ship if it collides with this specific bolt. If it does, the
        ship becomes None.

        Parameter bolt: the bolt that is tested if it collides with any ship
        Precondition: an alien bolt from the Bolt class
        """
        if self._ship != None:
            if self._ship.collides(bolt):
                self._ship = None
                self._bolts.remove(bolt)

    def invation(self):
        """
        Returns True when aliens end up invading under the defense line.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    lowest_alien = alien
        if lowest_alien.y - ALIEN_HEIGHT/2 <= DEFENSE_LINE:
            return True
        else:
            return False

    def gameOver(self):
        """
        Checks if the game is over by checking if
        (1) all the aliens are killed or
        (2) any alien dips below the defense line
        """
        if self._aliens == [[None]*ALIENS_IN_ROW]*ALIEN_ROWS:
            self._gameResult = True
            return True
        elif self._lives == 0 or self.invation():
            self._gameResult = False
            return True
