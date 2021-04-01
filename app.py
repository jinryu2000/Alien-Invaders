"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

Jin Ryu jfr224
December 4th 2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    self._storedlives = number of lives to start the game with
    self._alienspeed = alien speed of this wave
    self._score = score gained throughout the game
    """

    # DO NOT MAKE A NEW INITIALIZER!

    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._view = super().view
        self._input = super().input
        self._state = STATE_INACTIVE
        self._wave = None
        self._text = None

        self._storedlives = SHIP_LIVES
        self._alienspeed = ALIEN_SPEED
        self._score = 0

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_COMPLETE: The wave is over, and is either won or lost.

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._state == STATE_INACTIVE:
            self.INACTIVE()

        if self._state == STATE_NEWWAVE:
            self.NEWWAVE()

        if self._state == STATE_ACTIVE:
            self.ACTIVE(dt)

        if self._state == STATE_PAUSED:
            self.PAUSED()

        if self._state == STATE_CONTINUE:
            self.CONTINUE()

        if self._state == STATE_COMPLETE:
            self.COMPLETE()

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        text_states = [STATE_INACTIVE,STATE_ACTIVE,STATE_PAUSED,STATE_COMPLETE]
        if self._state in text_states:
            self._text.draw(self.view)

        wave_states = [STATE_NEWWAVE, STATE_ACTIVE, STATE_CONTINUE]
        if self._state in wave_states:
            self._wave.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def INACTIVE(self):
        """
        Updates Inavdorders when its state is STATE_INACTIVE.

        Before a wave has started, this method sets up Invader object for when
        its state is inactive.
        """
        self._wave = Wave(self._storedlives, self._alienspeed, self._score)

        text = "WELCOME! \nPRESS 'S' FOR SOME THRILL"
        x = GAME_WIDTH / 2
        y = GAME_HEIGHT / 2
        self.setText(text, x, y, 'Arcade.ttf', 0.063)

        if self._S_key_down():
            self._state = STATE_NEWWAVE

    def NEWWAVE(self):
        """
        Updates Inavdorders when its state is STATE_NEWWAVE.

        When it is time to create a new wave of aliens, this method get rids of
        previous state's text and allows transition into STATE_ACTIVE state.
        """
        self._text = None
        self._state = STATE_ACTIVE

    def ACTIVE(self, dt):
        """
        Updates Inavdorders when its state is STATE_ACTIVE.

        While the game is ongoing and the aliens are marching, this method
        displays current score and number of lives on the upper right corner of
        the screen. Also, it updates the wave object and score.
        When the game is over or the ship's lives left is zero, it allows
        Invadors's state transition into STATE_COMPLETE. If it is not over yet
        but the ship has collided, then this method decrements the number of
        lives left and allows Invadors's state transition into STATE_PAUSED.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        text = "Lives: " + str(self._storedlives)
        text +=  "\nScore: " + str(self._score)
        x = GAME_WIDTH/2
        y = GAME_HEIGHT/2
        right = GAME_WIDTH - 30
        top = GAME_HEIGHT - 10
        self.setText(text, x, y, 'RetroGame.ttf', 0.025, 'right', right, top)

        self._wave.update(dt, self.input)
        self._score = self._wave.getScore()

        if self._wave.gameOver():
            self._state = STATE_COMPLETE
        elif self._wave.getShip() == None:
            self._storedlives -= 1
            if self._storedlives != 0:
                self._text = None
                self._state = STATE_PAUSED
            else:
                self._state = STATE_COMPLETE

    def PAUSED(self):
        """
        Updates Inavdorders when its state is STATE_PAUSED.

        While the game is paused, this method displays a message. When 'S' key
        is pressed on keyboard, it allows transition into STATE_CONTINUE state.
        """
        text = "Ship is destroyed.. \nPRESS 'S' TO CONTINUE"
        x = GAME_WIDTH / 2
        y = GAME_HEIGHT / 2
        self.setText(text, x, y, 'TimesBoldItalic.ttf', 0.045)

        if self._S_key_down():
            self._state = STATE_CONTINUE

    def CONTINUE(self):
        """
        Updates Inavdorders when its state is STATE_CONTINUE.

        While the player is waiting for a new ship, this method sets a new ship
        and allows transition back into STATE_ACTIVE state.
        """
        self._wave.setShip()
        self._state = STATE_ACTIVE

    def COMPLETE(self):
        """
        Updates Inavdorders when its state is STATE_COMPLETE.

        When the game is over, this method displays a message demenstrating how
        this game ended: won or lost. In addition, if the player still has
        leftover lives but killed all the aliens, this method allows the player
        to get a new Wave by pressing 'S' key on the keyboard.
        """
        if self._wave.getResult():
            text = "YOU WON!" + "\nPress 'S' for more thrill"
            text += "\n \nScore: " + str(self._score)
            x = GAME_WIDTH / 2
            y = GAME_HEIGHT / 2
            self.setText(text, x, y, 'Arcade.ttf', 0.0625)
            if self._wave.getLives() > 0 and self._S_key_down():
                self._alienspeed *= (1/2)
                self._state = STATE_INACTIVE
        else:
            text = "Invaded by Aliens.. \nGOODBYE"
            text += "\n \nScore: " + str(self._score)
            x = GAME_WIDTH / 2
            y = GAME_HEIGHT / 2
            self.setText(text, x, y, 'TimesBoldItalic.ttf', 0.05)

    def _S_key_down(self):
        """
        Returns True if the 'S' key from keyboard is down.
        """
        if self.input.is_key_down('s'):
            return True
        else:
            return False

    def setText(self, text, x, y, fname, fsize, halign='center', r=None, t=None):
        """
        Creates a GLable text object and set it to the Invadors attribut _text.

        Parameters: keywords from initializing a GLabel object
        Precondition: follows precondition of each parameter from GLabel class
        """
        self._text = GLabel(text = text)
        self._text.x = x
        self._text.y = y
        self._text.font_name = fname
        self._text.font_size = fsize * GAME_WIDTH
        self._text.halign = halign
        if r != None and t != None:
            self._text.right = r
            self._text.top = t
