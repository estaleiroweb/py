import PySimpleGUI as sg
from cotacao import *
# https://www.pysimplegui.org/en/latest/#pysimplegui-users-manual

'PySimpleGUI,TkInter,PyQT5'

sg.theme('DarkAmber')   # Add a touch of color
# All the stuff inside your window.


class GUI:
    def __init__(
        self, title, layout=None, default_element_size=None,
        default_button_element_size=(None, None),
        auto_size_text=None, auto_size_buttons=None, location=(None, None), relative_location=(None, None), size=(None, None),
        element_padding=None, margins=(None, None), button_color=None, font=None,
        progress_bar_color=(None, None), background_color=None, border_depth=None, auto_close=False,
        auto_close_duration=sg.DEFAULT_AUTOCLOSE_TIME, icon=None, force_toplevel=False,
        alpha_channel=None, return_keyboard_events=False, use_default_focus=True, text_justification=None,
        no_titlebar=False, grab_anywhere=False, grab_anywhere_using_control=True, keep_on_top=None, resizable=False, disable_close=False,
        disable_minimize=False, right_click_menu=None, transparent_color=None, debugger_enabled=True,
        right_click_menu_background_color=None, right_click_menu_text_color=None, right_click_menu_disabled_text_color=None,
        right_click_menu_selected_colors=(None, None),
        right_click_menu_font=None, right_click_menu_tearoff=False,
        finalize=False, element_justification='left', ttk_theme=None, use_ttk_buttons=None, modal=False, enable_close_attempted_event=False,
        titlebar_background_color=None, titlebar_text_color=None, titlebar_font=None, titlebar_icon=None,
        use_custom_titlebar=None, scaling=None,
        sbar_trough_color=None, sbar_background_color=None, sbar_arrow_color=None, sbar_width=None, sbar_arrow_width=None, sbar_frame_color=None, sbar_relief=None,
        metadata=None
    ) -> None:
        kargs = locals()
        del (kargs['self'])
        self._event = None
        self._val = None
        self._call = {
        }
        self._win = sg.Window(**kargs)

    @property
    def event(self) -> str: return self._event
    @property
    def val(self) -> str: return self._val
    @property
    def call(self) -> str: return self._call
    @property
    def win(self) -> str: return self._win

    def loop(self) -> None:
        'Event Loop to process "events" and get the "values" of the inputs'
        while self._win:
            self._event, self._val = self._win.read()
            if sg.WIN_CLOSED == self._event:
                self.close()
                break
            if not self._event:
                continue
            fn = self._call.get(self._event)
            if fn and callable(fn):
                v = self._val.get(self._event) if self._val else None
                fn(self, self._event, v)

    def close(self, obj: 'GUI' = None, name: str = '', value=None) -> None:
        self._win.close()
        self._win = None

def getCotacao(obj: 'GUI', name: str, value):
    codMoeda=obj.val['nome_cotacao']
    d = cotacao(codMoeda)
    if d:
        print(d)
        v = f"{d['from']['symbol']}1.00={d['to']['symbol']}{d['bid']}"
    else:
        v = '<não encontrado>'
    obj.win['result'].update(v)
    # obj.close()

# print(cotacao())
# quit()

layout = [
    [sg.Text('Pega Cotação')],
    [sg.Text('Cotação: '), sg.InputText('USD',key='nome_cotacao')],
    [sg.Button('Ok'), sg.Button('Cancel',)],
    [sg.Text(key='result')],
]
# Create the Window
# window = sg.Window('Window Title', layout)

g = GUI('Window Title', layout)
g.call['Cancel'] = g.close
g.call['Ok'] = getCotacao
g.loop()
