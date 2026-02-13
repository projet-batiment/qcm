#!/usr/bin/env python

from ttkbootstrap import Window

from qcm.control.controller import Control
from qcm.utils.logs import setup_logging

import logging
logger = logging.getLogger(__name__)


if __name__ == "__main__":
    setup_logging(logging.DEBUG)
    logger.debug("Launching the application")

    window = Window(themename="flatly")
    window.title("QCM LPORM")
    window.geometry("900x700")

    logger.debug("Setting up the controller")
    Control(window)

    logger.debug("Starting main loop")
    window.mainloop()

    logger.debug("The main loop has stopped. Shutting down now.")
