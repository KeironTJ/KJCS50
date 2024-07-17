# KJCS50# KJCS50

# Keiron Jones Final CS50x Project 

## Project Title
Guess the Number

## Video URL
You can watch the project demo video "VIDEO URL WILL GO HERE"

## Project Description
"Guess the Number" is a web-based game designed as my final project for CS50x. The game challenges players to guess a randomly generated number within a specified range, offering hints based on their guesses to guide them towards the correct answer. This project was developed using Flask, a Python web framework, and incorporates HTML, CSS, and JavaScript for the frontend, with SQLite for data persistence.

### How the Game Works
Upon visiting the game's website, users are greeted with a simple interface asking them to input a guess within the given range. The game then responds with feedback, indicating whether the guess is too high, too low, or correct. Players can adjust their guesses based on this feedback until they find the correct number.

### Project Files and Structure
I opted for an App Factory model. This approach significantly enhances the modularization of the application, allowing for a logical separation of concerns across the codebase. This decision aligns with the overarching goal of creating a well-structured and easily navigable project.

app/
    __init__.py: Initializes the Flask application and configures the database.
    routes.py: Contains the routes for the game, including the main game page and settings.
    models.py: Defines the database models, including user settings for the game.
    /admin/
        decorators.py: Contains the logic for managing user access to specified admin pages
    /auth/
        routes.py: Handles user authentication (With help from The Flask Mega Tutorial)
    /game/
        game_logic.py: Contains the backend logic for generating the number, evaluating guesses, and providing hints.
    /main/
        routes.py: Handles any generic routing within the web application. 
templates/
    /admin/
        Collection of pages to display all admin available data. Limited to admins only.
    /auth/
        Contains all the pages to deal with user registration and authentication
    /game/
        guess_the_number_history.html: Allows uses to view their historic game progress
        guess_the_number_settings.html: Allows users to customize game settings, such as the number range
        guess_the_number.html: Main page for dealing with the game. 

    /main/
        base.html: Template used across all other pages for displaying navigation menu and managing Flash messages.
        index.html: The main game page template, displaying the game interface.
static/
    style.css: Custom CSS styles for the game's interface.
        
### Design Choices
One of the key design decisions made during the development of "Guess the Number" was to keep the game logic on the server side. This approach was chosen to prevent any potential cheating by inspecting client-side code. All guesses are sent to the server, which then evaluates them and returns the result. This ensures the game's integrity and fairness.

Another significant decision was to use SQLite for data persistence. Given the project's scope and the need for simplicity and portability, SQLite was an ideal choice. It allows for easy setup, doesn't require running a separate database server, and is more than capable of handling the data load for a project of this size.

### GameService
The GameService class is responsible for managing the game logic. It has an __init__ method that initializes the class with the following attributes,  user_guess, ainumber, user_guesses, user_id, start_range, and end_range. These attributes are used throughout the class to keep track of the game state and user inputs.

The check_guess method compares the user's guess (self.user_guess) with the randomly generated number (self.ainumber). If the guess is correct, it displays a success message using the flash function. If the guess is too low, it displays a danger message indicating that the guess is too low. If the guess is too high, it displays a danger message indicating that the guess is too high.

The save_guess method creates a new instance of the GuessTheNumberHistory model and saves it to the database using SQLAlchemy. This model represents a historical record of the game, including the user's ID, the range of numbers used in the game, the correct number, and the number of guesses made by the user.

The add_guess method appends the user's guess to the list of user_guesses stored in the session. The session is used to keep track of the user's guesses during the game.

The reset_game_session function resets the game session by setting the ainumber to 0 and clearing the user_guesses list. This function can be called when a new game is created.

The start_game_session function initializes the game session by retrieving the game settings from the database based on the user_id. If the settings are not found, it creates default settings with a start range of 1 and an end range of 100. It then generates a random number within the specified range and stores it in the session as ainumber. It also initializes an empty list for user_guesses in the session.

To summarize, the GameService class provides methods for checking the user's guess, saving the guess to the database, adding the guess to the session, and retrieving the guesses and the randomly generated number. The helper functions reset_game_session and start_game_session handle the initialization and resetting of the game session.

### Challenges and Solutions
One challenge faced during development was managing state between the client and server, especially when providing feedback for guesses. This was addressed by using session variables in Flask to store the current number to guess, as well as the range, ensuring that the game could track progress across multiple requests without requiring a database write for each guess.

## Conclusion
Developing "Guess the Number" for my CS50x final project was an immensely rewarding experience, allowing me to apply the skills I've learned in the course in a practical, fun project. This game not only demonstrates my understanding of web development principles but also my ability to create a complete, user-friendly application from scratch.

I hope players enjoy the game as much as I enjoyed creating it. Feedback and suggestions for future improvements are always welcome.


