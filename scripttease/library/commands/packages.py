# Classes


class Install(object):

    def __init__(self, name, manager="pip", overlay=None, upgrade=False, **kwargs):
        if overlay is not None:
            statement = overlay.get("package_install", manager, package_name=name, upgrade=upgrade)
        else:
            statement = "%s install %s" % (manager, name)

        self.statement = statement


class Remove(object):

    def __init__(self, name, manager="pip", overlay=None):
        if overlay is not None:
            statement = overlay.get("package_remove", manager, package_name=name)
        else:
            statement = "%s uninstall %s" % (manager, name)


