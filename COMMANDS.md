# Command Arguments

## Usage Schema

```bash
nonarrate [folder of .rpy files OR errors.txt] [options]
```

## Positional

**(folder of *.rpy* files OR *'errors.txt'* file)**

**Accepts**:

- Folder containing your `.rpy` files. **Recommend:** `game/` folder
- The `errors.txt` file

```bash
# Example project structure

MyRenpyProject/
├── game/
├── renpy/
├── launcher/
├── log.txt
├── errors.txt
├── saves/
```

**Notes:**

- If a `folder` is provided, *nonarrate* will operate on `.rpy` files located in subdirectories too.
- If `errors.txt` file is provided, *nonarrate* will *attempt* to fix the errors mentioned in the file.
  - **Nonarrate will not fix all errors!** See *[ERROR_TYPE.md](./ERROR_TYPES.md)* for list of fixes.
- If `errors.txt` file is provided, **all options you provide will be ignored!**
- **Typical workflow:**
  1. Use *nonarrate*
  2. Run game and get error message(s).
  3. Keep game running and use nonarrate on generated `errors.txt` file.
  4. Click **Reload**.
  - If more errors appear, Repeat steps 3 and 4
  > **OR**
  - **Debug** the issue yourself by taking advantage
  of the features nonarrate provides, which includes:
    - Ignoring files
    - Ignoring folders
    - Deactivating default narrator filters
    - Using regex for granular control *(on supported narrator filters)*

**Examples:**

This removes narration starting from *mycoolgame's* `game/` folder.

```bash
nonarrate C:\mycoolgame\game
```

This fixes the errors caused by the tool. *Point it to the generated `errors.txt`.*

```bash
nonarrate C:\mycoolgame\errors.txt
```

- - -

## Options

### General

***-p, —pauses***

Show removed narrated scenes by pausing.

*nonarrate* will replace narration with a
 [￼`pause`￼ statement](https://www.renpy.org/doc/html/quickstart.html#pause-statement).
This allows you to see narrated scenes without their dialogue
*(so you can see just the image/CG/animation/etc.)*.
To enable this feature, use this option.

**Side Note:** Since narrated dialogues are replaced by [￼`pause`￼ statements](https://www.renpy.org/doc/html/quickstart.html#pause-statement), there
are some instances where clicking to move forward *feels* like it does nothing.
In reality, the next sequence is *also* a pause statement.

***-b, --backup*** `<backup-path-directory>`

Backup *.rpy* files to a specified location.

Backup the project's *.rpy* files to a specified location *before* removing narration.

***-e, --regex***

Enable regular expressions when specifying filter values.

For filters that allow for user input, all values are treated as a regular expression.
See [REGEX Example](#regex-examples) for more info

***-j, --jobs*** `<number-of-threads>`

Maximum workers to use for I/O tasks.

Specify the maximum number of threads to handle all I/O operations.
`1 job = 1 thread`. **Default:** `min(32, CPU_COUNT * 4)`

___

### File Searching

***--invalid-dirs, --ind*** `<directory-name...>`

```bash
# While looking through 'mycoolgame\game' ignore directories: gui/, gamepad_control_schemes/, and cache helper/
nonarrate mycoolgame\game --invalid-dirs gui gamepad_control_schemes "cache helper"
```

Ignore specified folders when looking for *.rpy* files.

nonarrate will search subdirectories starting from the folder you point it to for
*.rpy* files. Use this option to prevent certain directories from being searched.

Nonarrate will ignore certain folders by default. See [IGNORED_FILES.md](./IGNORED_FILES.md) for list.

***--invalid-files, --inf*** `<filename...>`

```bash
# While looking through 'mycoolgame\game' ignore files named: options.rpy, image.rpy, keymap.rpy
nonarrate mycoolgame\game --invalid-files options image keymap
```

Ignore specified *.rpy* files when looking for *.rpy* files.

nonarrate will ignore the specified files when searching for *.rpy* files. Can
be used with `--invalid-globs`.

Nonarrate will ignore certain files by default. See [IGNORED_FILES.md](./IGNORED_FILES.md) for list

***NOTE: Do *not* include `.rpy`. nonarrate will automatically assume this file type!**

***--invalid-globs, --ing*** `<file-glob...>`

```bash
# ignore files matching: [0-9][0-9][a-zA-Z]*
# This pattern will match files such as 01animation.rpy, 93decor_tl.rpy, and 25TEST.rpy
nonarrate mycoolgame\game --invalid-globs '[0-9][0-9][a-zA-Z]*'
```

Ignore *.rpy* files using globs.

nonarrate will ignore files that match any of the specified file globs. Can be used
with `--invalid-files`. 

See [Python's fnmatch library](https://docs.python.org/3/library/fnmatch.html#module-fnmatch)
for list of available globs. **Globs**: `*`, `?`, `[...]`

***NOTE: Do *not* include `.rpy`. nonarrate will automatically assume this file type!**

___

### Narrator Filters

#### Character/Speaker

These filters deal with the **speaker** portion of a dialogue box.

| Commands                              | Script Example                                                                                                                          | Description                                                                                           |
|---------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------|
| --basic-char-obj                      | n = Character(“Narrator”, …)                                                                                                            | [Default narrators](#default-narrators) saved to character object.                                    |
| --no-custom-char-objs,<br>--ncco      | d = Character(“Developer”, …)                                                                                                           | Custom speaker saved to character object by their _in-game_ name. In this example, its `"Developer"`. |
| --basic-char                          | “Narrator” “It was a sunny day.”                                                                                                        | [Default narrators](#default-narrators) wrapped in quotes.                                            |
| --none-char-obj                       | narr = Character("", ‥)<br> narr = Character(None, ‥) <br> narr = Character() <br> narr = Character(Nothing in the `name` parameter, ‥) | Narrators using an empty character object. In short, nothing in the `name` parameter.                 |
| --no-custom-chars,<br>--ncc           | “Lily's Inner Self” “It would be a good idea to distract them first”                                                                    | Custom Speaker wrapped in quotes                                                                      |
| --no-custom-char-var-objs,<br>--nccvo | se = Character("Sue", …)                                                                                                                | Custom speaker saved to character object by their _variable_ name. In this example, its `se`.         |

***—basic-char-obj***

```bash
nonarrate mycoolgame\game --basic-char-obj 
```

Keep [default narrators](#default-narrators) saved to a `Character` object.

By default, *nonarrate*
will remove *all* [default narrators](#default-narrators) saved to a character object. Use this option to disable this filter.

***—no-custom-char-objs***, ***—ncco*** `<speaker name>...`

```bash
# Removes speakers: Wilson, Marisa, & Kyli Naya
nonarrate mycoolgame\game --no-custom-char-objs Wilson Marisa "Kyli Naya"
```

Removes speaker(s) saved to a `Character` object by their in-game name.

Sometimes, a narrator takes on the form of a character in game. Instead of being explicitly named *Narrator*, in-game,
the narrator can introduce itself as *Emily*, *Dev*, *The Chosen One*, or anything else… in-game.

**Side Note:** This option can use **REGEX**. Use `--regex` to enable this feature.  See [REGEX Examples](#regex-examples) for examples.

***—no-custom-char-var-objs***, ***—nccvo*** `<speaker name>...`

```bash
# Removes speakers whose variable names in an `.rpy` file are: nt, bik, naomi
nonarrate mycoolgame\game --no-custom-char-var-objs nt bik naomi
```

Removes speaker(s) saved to a `Character` object by their _variable_ name.

Sometimes it is easier to remove a narrator based on the variable's name the Character object is saved to.

To find the variable name, you must look into the `.rpy` files. A variable is defined as follows:
`define <variable-name> = Character` or `default <variable-name> = Character`.

**Side Note:** This option can use **REGEX**. Use `--regex` to enable this feature.  See [REGEX Examples](#regex-examples) for examples.

***—basic-char***

Keep [default narrators](#default-narrators) introduced in quotes.

Prevents *all* [default narrators](#default-narrators) explicitly written in quotes
alongside their dialogue from being removed. These types of narrators are
**NOT** saved to a `Character` object.

***--none-char-obj***

Keep empty Character objects.

Empty character objects, written as any of the following:

- `Character()`,
- `Character(None)`
- `Character("")`
- Or simply **NOT** using the [`name` parameter](<https://www.renpy.org/doc/html/dialogue.html#Character>), `Character(color="#FFFF00")`

These character objects are often either used as a blank speaker or are assigned
an actual speaker name later *(often used when renaming a character later in
the game.)*.

***—no-custom-chars***, ***—ncc*** `<speaker name>...`

```bash
# Removes speakers: Minie, Brock Lyn, & Carmi
nonarrate mycoolgame\game --no-custom-chars Minie "Brock Lyn" Carmi
```

Removes a speaker introduced in quotes.

Removes a speaker explicitly written in quotes alongside their dialogue and **NOT** saved to a `Character` object.

**Side Note:** This option can use **REGEX**. Use `--regex` to enable this feature.  See [REGEX Examples](#regex-examples) for examples.

- - -

#### Dialogue

These filters deal with the **dialogue** portion of dialogue box.

| Commands                | Script Example                                                                       | Description                                                                                                  |
|-------------------------|--------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| --basic-narr            | “I’m the narrator of this game”                                                      | Dialogues without a speaker                                                                                  |
| --italic-narr           | mc “{i}Maybe there’s food left over.{/i}" <br>mc "{tag}{i}Lesson learned!{/i}{/tag}" | Italics. Thinking dialogue.                                                                                  |
| --parenthesis-narr      | mc “(It’s got to be here somewhere.)” <br>mc "{tag}(Opens the car door){/tag}"       | `()`. Thinking/Narrator dialogue                                                                             |
| --no-custom-tags, --nct | mc “{fzs}A small bold font tag.{/fzs}” <br>mc "{fzs=10}My text is here{/fzs}"        | [Custom text tag.](https://www.renpy.org/doc/html/custom_text_tags.html) Can be used for thoughts/narrative. |
| --cues                  | mc "\**blushes softly*\*" <br>mc "{tag}\~*jumps*\~{/tag}"                            | Expression cues. \**smiles*\*, \~yawns\~, \*\**taps foot*\*\*                                                |
| --periods               | mc "......" <br>mc "{tag}..........{/tag}"                                           | Periods only dialogue                                                                                        |

***—basic-narr***

Keep dialogues that do not have a speaker.

Dialogues without a speaker are a clear indication of narration. Use this option if you want to keep this form
of narration.

***—italic-narr***

Keep dialogues that are fully italic.

Developers tend to use italics to indicate what a person is thinking about. Use this option to allow this feature.

***—parenthesis-narr***

Keep dialogues wrapped entirely in a parenthesis

Parentheses are used to indicate thoughts. It’s often used for narration.
Use this option to allow this feature.

***—no-custom-tags***, ***—nct*** `<tag name>...`

```bash
# Removes dialogues fully wrapped in either a {fzs}, {b}, or {color} tag
nonarrate mycoolgame\game --no-custom-tags fzs b color
```

Removes dialogue wrapped entirely in a custom text tag

Developers can create their own [custom text tags](https://www.renpy.org/doc/html/custom_text_tags.html), adding
custom style properties to them like `{color}` or `{font}`. Use this option to remove dialogue completely surrounded by a custom text tag.

This option also automatically removes the `=` variants of a custom text tag.

```bash
# Removes {fzs} and {fzs=<any-value-here>}
nonarrate mycoolgame\game --no-custom-tags fzs
```

**Side Note:** This option can use **REGEX**. Use `--regex` to enable this feature.  See [REGEX Examples](#regex-examples) for examples.

***--cues***

Keeps expression cues.

Keeps dialogue that *only* includes an expression cue.
Expression cues are signals indicating emotions and reactions. However,
this can be achieved *visually*.

Expression cue examples:

- \*smiles\*
- \~yawns\~
- \*crosses arms\*
- \*shakes head in disbelief\*
- \~burps loudly\~
- \*laughs maniacally\*
- \*\*rubs shoulder\*\*
- \*\*eats slowly\*\*

**--periods**

Keeps period only dialogue.

By default, dialogue consisting of only periods are removed. To keep them, use this option.

- - -

## Default Narrators

This is a list of common narrator names. *(includes capital case too)*

- thought
- thoughts
- thinking
- mind
- narrator

## REGEX Examples

*nonarrate* supports all regular expressions available in Python. See [Python REGEX Documentation](https://docs.python.org/3/library/re.html#regular-expression-syntax) for more info.

```bash
# Remove speakers: Wilson, Greyes, and Grayes character objects
nonarrate --no-custom-char-objs Wilson "Gr[ea]yes"

# Removes speakers: Temo, Temoes, Teemoes, & Teemo
nonarrate --no-custom-chars "Te{1,2}mo(es)?"

# Removes speakers: [mcname]
# Use '\\' to escape special characters.
nonarrate --no-custom-char-objs '\\[mcname\\]'
```
