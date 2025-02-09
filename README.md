# Foldy
A 1D programming language that doesn't stay 1D.

## Table of Contents
* [How to Run Foldy](#how-to-run-foldy)
* [How Foldy Works](#how-foldy-works)
* [Foldy Instructions](#foldy-instructions)

## How to Run Foldy
This Foldy interpreter runs via the command line. Type <code>py \_\_init\_\_.py <i>\<code\></i></code> to run <i>\<code\></i>.

You can also add on some flags:
* `-c` or `--check` lets you check that the code you typed in was correct. If you don't like the code, you can type `no` (case-insensitive).
* `-h` or `--help` gives you a list of all of the arguments and options.
* `-i` or `--iterations` lets you change how long the interpreter runs the code before giving up. By default, this is 50,000 ticks.

## How Foldy Works
Foldy is a 2D programming language. The *instruction pointer* (IP) starts in the upper-left corner, and runs to the right. If it hits a wall, it warps to the other side.

However, the code isn't allowed to have any line breaks. This is because of the `}` and `{` instructions. If the IP hits one of these, it folds the rest of the code in a straight line clockwise or counterclockwise. This is, obviously, where the language gets its name.

But we're missing one last piece of the puzzle. Currently, you might try to make a loop using the fold instructions, like this:
```
abc>defg}hij}klmn}opq
```
<!-- I am aware the align attribute is deprecated in HTML 5. However, this is the only way I could get this to work. -->
<p align="center">&downarrow;&downarrow;&downarrow;</p>

```
abc>defg}
   q    h
   p    i
   o    j
   }nmlk}
```

Unfortunately, when the IP hits the fold instructions again, it'll overwrite the existing instructions with spaces, ruining the loop. To fix this, the `#` instruction turns off *fold mode*. Now, when the IP encounters a fold instruction, it'll just turn instead.

## Foldy Instructions
Here's a table of the instructions Foldy has. No other characters are allowed in the code.
| Instruction          | Action                                                                              |
|:--------------------:| ----------------------------------------------------------------------------------- |
| <code>&blank;</code> | No-op                                                                               |
| `0` to `9`           | Push 0 to 9 to the stack                                                            |
| `+`                  | Add the top two values on the stack                                                 |
| `-`                  | Subtract the top two values on the stack                                            |
| `*`                  | Multiply the top two values on the stack                                            |
| `:`                  | Integer-divide the top two values on the stack. Blows up if dividing by 0           |
| `<` `>` `^` `v`      | Force the IP to go in a certain direction                                           |
| `/` `\` `\|` `_`     | Bounce the IP                                                                       |
| `$`                  | If the top item on the stack is greater than 0, skip the next instruction           |
| `?`                  | Replace the top of the stack with a random number in \$[0,\\,\text{top of stack})\$ |
| `{`                  | **If fold mode is on:** Fold the rest of the code counterclockwise                  |
| `{`                  | **If fold mode is off:** Turn counterclockwise                                      |
| `}`                  | **If fold mode is on:** Fold the rest of the code clockwise                         |
| `}`                  | **If fold mode is off:** Turn clockwise                                             |
| `!`                  | Print the top of the stack as a character                                           |
| `.`                  | Print the top of the stack as a number                                              |
| `;`                  | Get a character from input                                                          |
| `,`                  | Get a number from input                                                             |
| `@`                  | Terminate the code                                                                  |
| `&`                  | Duplicate the top of the stack                                                      |
| `~`                  | Pop the top of the stack                                                            |
| `[`                  | Move the top of the stack to the bottom                                             |
| `]`                  | Move the \$n^\text{th}\$ item on the stack to the top                               |
| `#`                  | Toggle fold mode. By default, this is on                                            |
