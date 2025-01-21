def init_app(gui):
    assert gui in ['pyside', 'tkinter']

    if gui == 'pyside':
        from fitspy.apps.pyside.main import init_app
    else:
        from fitspy.apps.tkinter.gui import init_app

    return init_app()


def end_app(gui, appli, app, dirname_res=None):
    assert gui in ['pyside', 'tkinter']

    if gui == 'pyside':
        from fitspy.apps.pyside.main import end_app
    else:
        from fitspy.apps.tkinter.gui import end_app

    end_app(appli, app, dirname_res=dirname_res)
