

from app.modules.core.install import Install as Install_Module


class TestingBase():

    __install_module = None

    def __init__(self):
        self.__install_module = Install_Module()

    def login(self):
        pass

    def install(self, data):

        if self.__install_module.is_installed():
            return True

        self.__install_module.set_app_data(
            data["app_name"],
            data["app_email"],
            data["app_url"]
        )
        self.__install_module.set_admin_data(
            data["admin_username"],
            data["admin_email"],
            data["admin_password"]
        )

        return self.__install_module.install()

    def uninstall(self):
        return self.__install_module.uninstall()
