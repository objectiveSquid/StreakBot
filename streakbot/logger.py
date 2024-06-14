import colorama
import logging


class ColoredFormatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: colorama.Fore.BLUE + colorama.Style.BRIGHT,
        logging.INFO: colorama.Fore.GREEN + colorama.Style.BRIGHT,
        logging.WARNING: colorama.Fore.YELLOW + colorama.Style.BRIGHT,
        logging.ERROR: colorama.Fore.RED + colorama.Style.BRIGHT,
        logging.CRITICAL: colorama.Fore.RED
        + colorama.Style.BRIGHT
        + colorama.Back.WHITE,
    }

    def format(self, record: logging.LogRecord):
        log_color = self.COLORS.get(record.levelno, "")
        formatted_message = super().format(record)
        return log_color + formatted_message + colorama.Style.RESET_ALL


_colorama_initialized = False


def configure_logging(level: int, use_colors: bool) -> None:
    global _colorama_initialized

    if use_colors:
        formatter_class = ColoredFormatter
    else:
        formatter_class = logging.Formatter

    if not _colorama_initialized and use_colors:
        colorama.init(autoreset=True)
        _colorama_initialized = True

    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_formatter = formatter_class(
        "%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s",
        datefmt="%H:%M:%S",
    )
    console_handler.setFormatter(console_formatter)

    logging.basicConfig(level=level, handlers=[console_handler])
