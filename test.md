## Hangman Lab Discussion
### Luka Mdivani lm378, Saad Lahrichi sl636
### 1/13/2022


### Original Code

 * What pieces of code help versus obscure your understanding?
 
 * What comments could be removed and replaced with better variable names or by calling shorter methods?

 * What Code Smells can you find?
   There were some mistakes like common results of if() and else() statements which could be moved out of the conditionals.


### Extracting Player Classes

Which class (HangmanGame, Guesser, or SecretKeeper) should be responsible for these instance variables (and why): mySecretWord, myNumGuessesLeft, myDisplayWord, and myLettersLeftToGuess?

 * Game class code:
    - [x] Same
   
   * Different


 * ```play()``` method:
    - [x] ``` Game ```
   
   * ```Guesser```
   
   * ```SecretKeeper```
   

 * ```makeGuess()``` method:
   * ```Game```

    - [x] Guesser
   
   * ```SecretKeeper```
   


 * Which class should be responsible for each instance variable (and why):
   * ```mySecretWord```
   
   * ```myNumGuessesLeft```
   
   * ```myDisplayWord```



### Making Game Between New Kinds of Players

 * OLD CODE: What lines of a current ```Game``` class need to be changed to implement a hangman.game between two new players.

 * NEW CODE: What lines of the ```Player``` classes need to be changed to implement new players.

 * NEW CODE: What lines of the ```hangman.Main``` class need to be changed to implement a hangman.game between any two kinds of players.



### Refactored Code

 * In what ways is the refactored code simpler?

 * In what ways is the refactored code more complex?

 * What trade-offs did you make when refactoring the original code?

 * Which code do you prefer and why?
