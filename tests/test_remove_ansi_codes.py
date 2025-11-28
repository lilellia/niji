from niji import RGBColor, TextStyle, colored, remove_ansi_codes


def test_remove_ansi_codes_when_there_are_no_codes():
    assert remove_ansi_codes("some normal string") == "some normal string"


def test_remove_ansi_codes_when_codes_present():
    s = colored("some text", fg=RGBColor(13, 148, 43), bg=RGBColor(123, 44, 190),
                styles=TextStyle.BOLD | TextStyle.ITALIC)

    assert remove_ansi_codes(s) == "some text"
