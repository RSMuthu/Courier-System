from courier.utils import red, yellow, green, cyan


def test_console_red():
    assert "\033[91mhello\033[0m" == red("hello")


def test_console_yellow():
    assert "\033[93mhello\033[0m" == yellow("hello")


def test_console_green():
    assert "\033[92mhello\033[0m" == green("hello")


def test_console_cyan():
    assert "\033[96mhello\033[0m" == cyan("hello")
