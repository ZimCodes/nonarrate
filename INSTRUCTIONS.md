# Instructions

This section explains how to use nonarrate effectively **step-by-step**.

## Extract .rpa files

***This is an optional step**. If your game project does not have an `*.rpa` file located in the `game/` folder, skip
ahead.

`.rpa` files usually contain all assets to a game project. Nonarrate will only operate on `.rpy` files,
which can be found inside an `rpa` file. To get the assets, you will need to extract the `rpa` file(s).

There are many extractor tools you can use for this. Happy Hunting!

## Dialogue searching

Once you have access to the `.rpy` files in your `game/` folder, the next step is to search for files containing
**character definitions** and/or **dialogue**. *Keep note of these files!*

### Character Definitions

Speaker names are most often saved to a `Character(...)` object.
**Any `.rpy` file containing character definitions are a *must* for nonarrate.**

**Examples:**

See [Ren'Py Docs Examples](https://www.renpy.org/doc/html/dialogue.html#example-characters)

```python
define h = Character("Harold")
default m = Character("Mikaeil", what_italic=True)
```

### Dialogue

**Any `.rpy` file containing dialogue is a *must* for nonarrate.**

**Examples:**
See ['Say Statement' in Ren'Py's Docs](https://www.renpy.org/doc/html/dialogue.html#say-statement)

## Using nonarrate

Once you which `.rpy` files contain **character definitions** and **dialogue**, you can now use nonarrate.

It's recommended to use `--backup` alongside your commands which will create a backup of modified `.rpy` files.

**Example:**

```bash
nonarrate --invalid-files minigame opt --keep-empty-quoted-chars --backup ./MYBACKUP
```

### Ignoring files

Take advantage of the following options to tell nonarrate what files/folders to ignore or focus
on. [FILE COMMANDS](./COMMANDS.md#file-searching). **Be mindful! Nonarrate will ignore certain files/folders by default
*. See [IGNORED_FILES.md](./IGNORED_FILES.md).

```bash
nonarrate game/ --invalid-dirs images sfx --invalid-files red_shaders minigames --backup ./MYBACKUP
```

### Adjusting Narration

Sometimes, the default settings is not enough or maybe *too* much. Regardless, take advantage of
[Narrator Filter options](./COMMANDS.md#narrator-filters). Most often than not, simply enabling, `--keep-empty-quoted-chars` or
using `--text-tags <tags..>` to remove dialogue with certain tag names is all you need!

Additionally, pay attention to the tables provided in the [COMMANDS.md](./COMMANDS.md#narrator-filters). They will help you!

### Error Fixing

***This is an optional step**. In your case, the game may run smoothly. If so, you're done! Otherwise, continue reading this section.

When launching the game, an error screen will appear showing all the issues caused by nonarrate. Don't fret! This is
normal behavior. nonarrate comes with error fixing capabilities. Not all types of errors will be fixed. Check
out [ERROR_TYPES](./ERROR_TYPES.md) for eligible types.

To fix errors, point nonarrate to the auto-generated `errors.txt` file.

**Example:** `nonarrate ./errors.txt`

From here, there are 2 workflows you can use to reload the game:

1. *(recommended)* Keep error screen open and just select the `Reload` button
2. Close error screen and reopen game

Repeat these steps until the game is launched successfully!

## Final Thoughts

The key is finding files containing dialogue and adjusting narration to fit the current game's needs.
Every game project is different after all!
