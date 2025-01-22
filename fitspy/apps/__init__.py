def init_app(gui):
    from fitspy.apps.pyside.main import init_app as init_app_pyside
    from fitspy.apps.tkinter.gui import init_app as init_app_tkinter
    return eval(f"init_app_{gui}()")


def end_app(gui, appli, app, dirname_res=None):
    from fitspy.apps.pyside.main import end_app as end_app_pyside
    from fitspy.apps.tkinter.gui import end_app as end_app_tkinter
    end_app = eval(f"end_app_{gui}")
    return end_app(appli, app, dirname_res=dirname_res)


def fitspy_launcher(gui='pyside', fname_json=None, dirname_res=None):
    appli, qapp = init_app(gui)
    if fname_json is not None:
        appli.reload(fname_json)
    end_app(gui, appli, qapp, dirname_res=dirname_res)
