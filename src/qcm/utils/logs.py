import logging

from typing import Union
LogLevel = Union[int, str]

logger = logging.getLogger(__name__)

# count the calls to setup_logging
call_counter = 0


def setup_logging(level: LogLevel = logging.INFO) -> None:
    """
    Set the application-wide logging settings.
    Should only be run once during the execution.
    """

    global call_counter
    call_counter += 1

    logging.basicConfig(
        level=level,
        format="%(asctime)s: %(name)s [%(levelname)s]: %(message)s",
    )

    if call_counter > 1:
        match call_counter:
            case 2:
                suffix = "nd"
            case 3:
                suffix = "rd"
            case _:
                suffix = "th"

        logging.warning(f"setup_logging should only be called once (this is the {call_counter}{suffix} call)")
