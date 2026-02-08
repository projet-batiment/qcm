from logging import info
from tkinter import Frame

from control import AppState
from vue import MenuBar, question, splashscreen


class Control:
    def __init__(self, window):
        self.appstate = AppState.SPLASH_SCREEN

        self.states = {
            AppState.SPLASH_SCREEN: splashscreen.MainView(window),
            AppState.EDIT: question.MainView(window),
        }

        window.config(menu=MenuBar(window, self))

        self.current_state: Frame = None
        self.set_appstate(AppState.SPLASH_SCREEN)

    def set_appstate(self, appstate: AppState):
        if appstate not in self.states:
            raise ValueError(f"Not a known state: {appstate}")

        if self.current_state is not None:
            self.current_state.pack_forget()

        self.current_state = self.states[appstate]
        self.current_state.pack(fill="both", expand=True)

    def new_file(self):
        self.set_appstate(AppState.EDIT)

        self.states[AppState.EDIT].set_qcm_new()

    def open_file(self):
        info("ouvrir qcm")

    def save_file(self):
        info("sauvegarder qcm")
