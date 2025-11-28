# niji

From Japanese 虹 *niji*, meaning "rainbow".

The purpose of this package is to provide coloration of text in the terminal. It defaults behaviour to truecolor/24bit (
full RGB) color, but can gracefully downgrade when this is not supported by the terminal.

The two main functions provided are:

- `colored(text, *, fg, bg, styles, mode=TRUECOLOR) -> str` , which returns a string with the necessary ANSI codes
  injected for later manipulation and printing.
- `cprint(text, *, fg, bg, styles, mode=AUTO, file=sys.stdout) -> None`, which is a convenience wrapper around
  `print(colored(...))`.

## Examples

```python
from niji import colored, cprint, TextStyle

# use `colored` to style text, getting a string back
# this will always use truecolor sequences unless overridden
green_text = colored("some green text", fg=(0, 100, 0))
blue_on_purple = colored("blue text on purple background", fg=(0, 0, 100), bg=(100, 0, 100))
italic_bold_red = colored("colored also takes hex colors", fg="#aa0000", styles=TextStyle.ITALIC | TextStyle.BOLD)
close_enough = colored("use a color that's as close as a 256-color terminal can use", fg="#AE03B8",
                       mode=ColorMode.EXTENDED_256)

# use `cprint` when you want to print directly
# it will automatically handle the ColorMode
cprint("let's do... pink this time", fg="#C05ADC", styles=TextStyle.UNDERLINE)
with open("/path/to/some/file", encoding="utf-8") as f:
    cprint("you can write to a file, and colors will be suppressed", fg=(17, 12, 14), file=f)

cprint("even on a 256-color term, this will use the truecolor codes", fg=(0, 255, 0), mode=ColorMode.TRUE_COLOR)

# use `aware_colored` for a mix of the two
with open("/path/to/some/file", encoding="utf-8") as f:
    store_for_later = aware_colored("blue on red... except it'll be plain text", fg="#0000FF", bg="#FF0000", file=f)
    f.write("normal text" + store_for_later)
```

## Why `niji` instead of `termcolor`?

The main benefit is that `niji` strives to be more optimistic and explicit about its settings. Truthfully, I've used
`termcolor` for a long time and rarely had issues with it. But I had a situation like

```shell
# works just fine, producing the blue text 
$ python -c "from termcolor import cprint; cprint('some text', '#0000aa')"

# doesn't work (no color output) even though less -R supports it
$ python -c "from termcolor import cprint; cprint('some text', '#0000aa')" | less -R
```

which I expected to maintain the colors. I, as the person writing the code, knew that the colors were safe to emit, and
`termcolor` was adhering to the standard that colors should not be automatically written through a pipe (a convention I
wasn't aware of). I'd previously used `ripgrep` in a similar fashion, but `rg --color=always` is an easy way around
that. `termcolor` doesn't seem to support the same level of override (without setting an environment variable).

So `niji` aims to provide the user the explicit option to say "hey, I always want you to output color, regardless of
context". And thus the above example could be

```bash
# does emit colors properly
# (I know I'm using a truecolor terminal, but I could change the mode to EXTENDED_256 if I wasn't)
$ python -c "from niji import cprint, ColorMode; cprint('some text', fg='#0000aa', mode=ColorMode.TRUE_COLOR)" | less -R

# this also works and is a bit shorter, relying on the default mode value for colored since I know truecolor is safe
$ python -c "from niji import colored; print(colored('some text', fg='#0000aa'))"
```

## Installation

This library can easily be installed by any Python package manager and does not incur any other external dependencies.

```shell
$ pip install niji

# to test installation (#FF000 should be supported regardless of terminal)
$ python -c "from niji import cprint; cprint('a red hello world!', fg='#FF0000')"
```

Alternatively, using `uv` as a different example, the above two commands are:

```shell
$ uv add niji
$ uv run python -c "from niji import cprint; cprint('a red hello world!', fg='#FF0000')"
```

### Supported Python Versions

All versions of Python from 3.10 onward are supported. At the time of development (late 2025), 3.9 has been declared
end-of-life.

## Known Limitations

- Hex color parsing does not support shorthand codes (such as `#ABC` to mean `#AABBCC`.)
- `TextStyle` combinations (such as `TextStyle.ITALIC | TextStyle.UNDERLINE`) is known to produce type warnings in
  PyCharm.
  In this case, the warning is
  `Unexpected type(s): (Literal[TextStyle.UNDERLINE]) Possible type(s): (Literal[TextStyle.ITALIC]) (Literal[TextStyle.ITALIC])`.
  This is a limitation within PyCharm's handling of standard library `enum.Flag`. These warnings are not raised by mypy
  or Pyright/Pylance and **are safe to ignore**.

## Documentation

### `ColorMode`

`niji` supports injecting various versions of ANSI codes, depending on the capabilities of the terminal emulator. Some,
like `kitty`, support full 24bit RGB colors, while others, like `konsole`, only support the 256 indexed colors.
`ColorMode` is what controls which version of the codes is injected.

`ColorMode` is an enum with the following values:

- `ColorMode.TRUE_COLOR`: denotes the usage of full 24-bit "truecolor" codes. In this mode, colors will be rendered
  exactly as provided. This is the default value passed to `colored`.
- `ColorMode.EXTENDED_256`: denotes the usage of the full 8-bit (256 color) block of colors. This is a common minimum
  standard for modern terminal emulators.
- `ColorMode.STANDARD_16`: denotes the usage of the minimal 4-bit (16 color) block of colors (black, red, etc.) and
  their bright versions.
- `ColorMode.NONE`: denotes the omission of colors. This might be rare to set manually, but it provides an ability to
  omit colors when necessary (such as when writing to a file).
- `ColorMode.AUTO`: denotes auto-detection of available capabilities. This is only supported by `cprint` and
  `aware_colored`, as they have information about where the string is being written.

With `ColorMode.EXTENDED_256` and `ColorMode.STANDARD_16`, any truecolor colors passed to `colored`, `aware_colored`,
and `cprint` will be gracefully downgraded to the nearest indexed color, providing an "as good as possible" rendering.

Note that `colored(...)` takes `ColorMode.TRUE_COLOR` as an optimistic default. This is because the purpose of `colored`
is to designed to return a string that formats the text according to the given styles, and truecolor guarantees doing
that with optimal fidelity.

By contrast, `aware_colored(...)` and `cprint(...)` use `ColorMode.AUTO` as their default since their priority is to
more conservatively render the text as well as they can, given the constraints of the terminal (their `file` parameter).

### `TextStyle`

`TextStyle` is an enum flag that allows for additional formatting styles on top of colors. The full list of members are
`TextStyle.NONE`, `TextStyle.BOLD`, `TextStyle.DIM`, `TextStyle.ITALIC`, `TextStyle.UNDERLINE`, `TextStyle.BLINK`,
`TextStyle.REVERSE` (swap fg and bg colors), `TextStyle.CONCEALED` (hide text), `TextStyle.STRIKEOUT`.

Because this is an `enum.Flag`, these can be combined via `|` operations: `TextStyle.DIM | TextStyle.STRIKEOUT` will
render as both dim and strikeout text.

Note that `TextStyle.NONE` gets absorbed by this process: `TextStyle.DIM | TextStyle.NONE` is equivalent to just
`TextStyle.DIM`.

### `RGBColor`

`RGBColor` is a thin `typing.NamedTuple` that has `.red`, `.green`, and `.blue` attributes. It is used internally for
representing different colors, but is provided to the user as a top-level name (`from niji import RGBColor`) for
convenience.

### `ColorInput`

`ColorInput` is a type alias for `int | str | tuple[int, int, int] | RGBColor | Sequence[int]`.

- `int`: color is interpreted as an indexed color according to the 256 color map
- `str`: color is interpreted as a hex code (with or without a leading \#). Shorthand codes are not supported.
- `tuple[int, int, int] | RGBColor`: color is interpreted as an (R, G, B) tuple. These values must be ints, not floats (
  e.g., `(4.0, 5.0, 9.0)` is invalid).
- `Sequence[int]`: same as above, provided separately to allow other containers (such as `list[int]`). This must be a
  sequence of length 3.

### `colored` vs `aware_colored`

These two functions have very similar signatures:

```python
def colored(
        text: str,
        *,
        fg: ColorInput | None = None,
        bg: ColorInput | None = None,
        styles: TextStyle | None = None,
        mode: ColorMode = ColorMode.TRUE_COLOR
) -> str:
    ...


def aware_colored(
        text: str,
        *,
        fg: ColorInput | None = None,
        bg: ColorInput | None = None,
        styles: TextStyle | None = None,
        mode: ColorMode = ColorMode.AUTO,
        file: TextIO = sys.stdout
) -> str:
    ...
```

The difference is that `aware_colored` accepts `ColorMode.AUTO` as a valid option (and it's the default), allowing it to
query the passed `file` parameter to determine what type of codes it should use. Note that it still doesn't write to the
file (use `cprint` for that).




