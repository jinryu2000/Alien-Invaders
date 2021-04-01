"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new
class when you add extra features to an object. So technically Bolt, which has a velocity,
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you
add new features to your game, such as power-ups.  If you are unsure about whether to
make a new class or not, please ask on Piazza.

Jin Ryu jfr224
December 4th 2018
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.

    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.

    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self):
        """
        Creates a new ship.

        This method inherits the initializer method from class GImage.
        """
        h_pos = GAME_WIDTH / 2
        v_pos = SHIP_BOTTOM + SHIP_HEIGHT / 2
        w = SHIP_WIDTH
        h = SHIP_HEIGHT
        s = 'ship.png'

        super().__init__(x=h_pos, y=v_pos, width=w, height=h, source=s)

    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self,bolt):
        """
        Returns True if the bolt was fired by the player and collides with
        this alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert not bolt.isPlayerBolt()

        x = [bolt.x - BOLT_WIDTH/2, bolt.x + BOLT_WIDTH/2]
        y = [bolt.y - BOLT_HEIGHT/2, bolt.y + BOLT_HEIGHT/2,]

        for h_edge in x:
            for v_edge in y:
                if self.contains((h_edge, v_edge)):
                    return True
        return False


    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.

    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.

    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of
    putting it here is that Ships and Aliens collide with different bolts.  Ships
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not
    Alien bolts. An easy way to keep this straight is for this class to have its own
    collision method.

    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    _source: the source file for this image
    Precondition: a string refering to a valid file
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def setImage(self, row):
        """
        Returns a source image for the alien.

        Parameter row: the row in which the alien locates
        Precondition: an integer between 1 <= row <= ALIEN_ROWS
        """
        rowRange = ALIEN_ROWS
        sourceNumber = 0
        while rowRange > 0:
            rowRange -= 2
            if row > rowRange and rowRange+2 >= row:
                i = sourceNumber
            sourceNumber += 1

        index = i % len(ALIEN_IMAGES)
        return ALIEN_IMAGES[index]

    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, row, col):
        """
        Creates a new alien.

        This method inherits the initializer method from class GImage.

        Parameter row: the row in which the alien locates
        Precondition: an integer between 1 <= row <= ALIEN_ROWS

        Parameter col: the column in which the alien locates
        Precondition: an integer between 1 <= col <= ALIENS_IN_ROW
        """
        s = self.setImage(row)

        h_pos = col * ALIEN_H_SEP + (ALIEN_WIDTH/2) * (1 + 2*(col-1))
        v_pos = GAME_HEIGHT - ALIEN_CEILING - ALIEN_V_SEP * (row-1)
        v_pos -= (ALIEN_HEIGHT/2) * (1 + 2*(row-1))
        w = ALIEN_WIDTH
        h = ALIEN_HEIGHT

        super().__init__(x=h_pos, y=v_pos, width=w, height=h, source=s)

    # METHOD TO CHECK FOR COLLISION (IF DESIRED)
    def collides(self,bolt):
        """
        Returns True if the bolt was fired by the player and collides with
        this alien.

        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        assert bolt.isPlayerBolt()
        x = [bolt.x - BOLT_WIDTH/2, bolt.x + BOLT_WIDTH/2]
        y = [bolt.y - BOLT_HEIGHT/2, bolt.y + BOLT_HEIGHT/2]

        for h_edge in x:
            for v_edge in y:
                if self.contains((h_edge, v_edge)):
                    return True
        return False


class Bolt(GRectangle):
    """
    A class representing a laser bolt.

    Laser bolts are often just thin, white rectangles.  The size of the bolt is
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.

    The class Wave will need to look at these attributes, so you will need getters for
    them.  However, it is possible to write this assignment with no setters for the
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.

    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a
    helper.

    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.

    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _whichAlien: The alien from which the bolt is fired [Alien object]
        _whenToFire: The number of alien steps required to fire the bolt [int]
        _state: The state of the alien bolt, either 'active' or 'inactive' [str]
    """

    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getWhenToFire(self):
        """
        Returns the bolt attritbue _whenToFire.
        """
        return self._whenToFire

    def getWhichAlien(self):
        """
        Returns the bolt attritbue _whichAlien.
        """
        return self._whichAlien

    def setBoltState(self, state):
        """
        Returns the bolt attritbue _state.

        Parameter state: state of the alien bolt being fired or not
        Precondition: a string, either 'active' or 'inactive'
        """
        self._state = state

    def getBoltState(self):
        """
        Returns the bolt attritbue _state.
        """
        return self._state

    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, which, strwhich, when=None):
        """
        Creates a bolt.

        This method inherits the initializer method from class GRectangle.

        Parameter which: the object from which this alien bolt is fired
        Precondition: either a Ship object or an Alien object

        Paramter strwhich: a string that indicates what kind of object is firing
        Preconditon: a string, either 'ship' or 'alien'

        Parameter when: number of alien steps required to fire the alien bolt
        Precondition: an int between 1 <= when <= BOLT_RATE
        """
        if strwhich == 'ship':
            self._velocity = BOLT_SPEED
            Y = SHIP_BOTTOM + SHIP_HEIGHT + BOLT_HEIGHT/2

        elif strwhich == 'alien':
            self._velocity = -BOLT_SPEED
            self._whichAlien = which
            self._whenToFire = when
            self._state = 'inactive'
            Y = which.y - ALIEN_HEIGHT/2

        X = which.x
        w = BOLT_WIDTH
        h = BOLT_HEIGHT
        c1 = 'black'
        c2 = 'blue'

        super().__init__(x=X,y=Y,width=w,height=h,fillcolor=c1,linewidth=1,linecolor=c2)

    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def isPlayerBolt(self):
        """
        Returns True if this bolt from the player's ship. If not, returns False.
        """
        if self._velocity > 0:
            return True
        else:
            return False


# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE
