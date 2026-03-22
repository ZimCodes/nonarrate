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
MyRenpyProject/
├── game/
├── renpy/
├── launcher/
├── log.txt
├── errors.txt
├── saves/
```

**Notes:**

- If a `folder` is provided, *nonarrate* will operate on `.rpy` files located in subdirectories.
- If `errors.txt` file is provided, *nonarrate* will attempt to fix the errors mentioned in the file.
- If `errors.txt` file is provided, **all options you provide will be ignored!**

**Examples:**

This removes narration from *mycoolgame* `game/` folder.

```bash
python nonarrate C:\mycoolgame\game
```

This fixes the errors caused by the tool.

```bash
python nonarrate C:\mycoolgame\errors.txt
```

- - -

## Options

### General

***-p, —pauses***

Show narrated scenes stripped of narration by pausing.

*nonarrate* will replace narration with a
 [￼`pause`￼ statement](https://www.renpy.org/doc/html/quickstart.html#pause-statement).
This allows you to see narrated scenes without their dialogue
*(so you can see just the image/CG/animation/etc.)*.
To disable this feature, use this option.

**Side Note:** Since narrated dialogues are replaced by pause statements, there
are some instances when clicking to move forward *feels* like it does nothing.
In reality, the next sequence is *also* a pause statement.

***-b, --backup*** `<backup-path-directory>`

Backup *.rpy* files to a specified location.

Backup the project's *.rpy* files to a specified location before removing narration.

***-e, --regex***

Enable regular expressions when specifying filter values.

For filters that allow for user input, all values are treated as a regular expression.
See [REGEX Example](#regex-examples) for more info.

### File Filters

***--invalid-dirs***

```bash
# While looking through 'mycoolgame\game' ignore directories: gui/, gamepad_control_schemes/, and cache/
nonarrate mycoolgame\game --invalid-dirs gui gamepad_control_schemes "cache"
```

Ignore specified folders when looking for *.rpy* files.

nonarrate will search subdirectories starting from the folder you point it to for
*.rpy* files. Use this option to prevent certain directories from being entered.

***--invalid-files***

```bash
# While looking through 'mycoolgame\game' ignore files named: options.rpy, image.rpy, keymap.rpy
nonarrate mycoolgame\game --invalid-files options.rpy image.rpy keymap.rpy
```

Ignore specified files when looking for *.rpy* files.

nonarrate will ignore the specified files when searching for *.rpy* files.

### Narrator Filters

#### Character/Speaker

| Commands                         | Script Example                                             | Description                                                         |
|----------------------------------|------------------------------------------------------------|---------------------------------------------------------------------|
| no-basic-char-obj               | n = Character(“Narrator”, …)                               | [Default narrators](#default-narrators) saved to character object.                                 |
| custom-char-obj,<br>cco | d = Character(“Developer”, …)                              | Custom speaker saved to character object |
| no-basic-char                      | “Narrator” “It was a sunny day.”                           | [Default narrators](#default-narrators) wrapped in quotes. |
| no-none-char-obj | narr = Character("") / narr = Character(None) / narr = Character() | Narrators using an empty character object. |
| custom-char,<br>cc      | “My Mind” “It would be a good idea to distract them first” | Custom Speaker wrapped in quotes |

***—no-basic-char-obj***

```bash
nonarrate mycoolgame\game --no-basic-char-obj 
```

Do **not** remove [default narrators](#default-narrators) saved to a `Character` object.

In Ren’Py, it’s recommended to define speakers in a [
`Character()`](https://www.renpy.org/doc/html/dialogue.html#defining-character-objects) object. By default, *nonarrate*
will remove all [default narrators](#default-narrators) saved to a character object. Use this option to disable this filter.

***—custom-char-obj***, ***—cco*** `<speaker name>...`

```bash
# Removes speakers: Wilson, Marisa, & Kyli Naya
nonarrate mycoolgame\game --custom-char-obj Wilson Marisa "Kyli Naya"
```

Removes speaker(s) saved to a `Character` object.

Sometimes, a narrator takes on the form of a character in game. Instead of being explicitly named *Narrator*, the
narrator can introduce itself as *Emily*, *Dev*, *The Chosen One*, or anything else…

**Side Note:** This option can use **REGEX**. Use `--regex` to enable this feature.  See [REGEX Examples](#regex-examples) for examples.

***—no-basic-char***

Do not remove [default narrators](#default-narrators) introduced in quotes.

Prevents all [default narrators](#default-narrators) explicitly written
alongside their dialogue from being removed. These types of narrators are
**NOT** saved to a `Character` object.

***--no-none-char-obj***

Do not remove narrator objects with empty Character objects.

Empty character objects, written as `Character(), Character(None), or Character("")`,
are often saved and either used as blank speakers or are later assigned an
actual speaker name *(especially used when naming the main character later in
the game.)*. This option prevents these character objects from being removed.

***—custom-char***, ***—cc*** `<speaker name>...`

```bash
# Removes speakers: Minie, Brock Lyn, & Carmi
nonarrate mycoolgame\game --custom-char Minie "Brock Lyn" Carmi
```

Removes a speaker introduced in quotes.

Removes a speaker explicitly written alongside their dialogue and **NOT** saved to a `Character` object.

**Side Note:** This option can use **REGEX**. Use `--regex` to enable this feature.  See [REGEX Examples](#regex-examples) for examples.

- - -

#### Dialogue

| Commands             | Script Example                                 | Description                                                                                                  |
|----------------------|------------------------------------------------|--------------------------------------------------------------------------------------------------------------|
| —no-basic-narr       | “I’m the narrator of this game”                | Dialogues without a speaker                                                                                  |
| —no-italic-narr      | mc “{i}Maybe there’s food left over.{/i}       | Italics. Thinking dialogue.                                                                                  |
| —no-parenthesis-narr | mc “(It’s got to be here somewhere.)”          | `()`. Thinking/Narrator dialogue                                                                             |
| —custom-tag, —ct     | mc “{fzs}A small bold font tag.{/fzs}” <br>mc "{fzs=10}My text is here{/fzs}"| [Custom text tag.](https://www.renpy.org/doc/html/custom_text_tags.html) Can be used for thoughts/narrative. |

***—no-basic-narr***

Do **not** remove dialogues that do not have a speaker

Dialogues without a speaker are a clear indication of narration. Use this option if you want to keep this form
of narration.

***—no-italic-narr***

Do **not** remove dialogues that are fully italic

Developers tend to use italics to indicate what a person is thinking about. Use this option to allow this feature.

***—no-parenthesis-narr***

Do **not** remove dialogue wrapped entirely in a parenthesis

Parentheses are used to indicate thoughts. It’s often used for narration.
Use this option to allow this feature.

***—custom-tag***, ***—ct*** `<tag name>...`

```bash
# Removes dialogues fully wrapped in either a {fzs}, {b}, or {color} tag
nonarrate mycoolgame\game --custom-tag fzs b color
```

Removes dialogue wrapped entirely in a custom text tag

Developers can create their own [custom text tags](https://www.renpy.org/doc/html/custom_text_tags.html), adding
custom style properties to them like `{color}` or `{font}`. Use this option to remove dialogue completely surrounded by a custom text tag.

**Side Note:** This option can use **REGEX**. Use `--regex` to enable this feature.  See [REGEX Examples](#regex-examples) for examples.

- - -

## Default Narrators

This is a list of common narrator names.

- thought
- thoughts
- thinking
- mind
- narrator

## REGEX Examples

*nonarrate* supports all regular expressions available in Python. See [Python REGEX Documentation](https://docs.python.org/3/library/re.html#regular-expression-syntax) for more info.

```bash
# Remove speakers: Wilson, Greyes, and Grayes character objects
nonarrate --custom-char-obj Wilson "Gr[ea]yes"

# Removes speakers: Temo, Temoes, Teemoes, & Teemo
nonarrate --custom-char "Te{1,2}mo(es)?"

# Removes speakers: [mcname]
# Use '\\' to escape special characters.
nonarrate --custom-char-obj '\\[mcname\\]'
```
