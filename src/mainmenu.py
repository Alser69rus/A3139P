from src.asemenu import Menu, MenuItem


class Ui_MainMenu(object):
    def setupMenu(self, MainWindow):
        MainWindow.main_menu = MainMenu()
        MainWindow.menu.addMenu(MainWindow.main_menu)
        MainWindow.ku215 = MenuKU215()
        MainWindow.menu.addMenu(MainWindow.ku215)
        MainWindow.btp020 = MenuBTP020()
        MainWindow.menu.addMenu(MainWindow.btp020)
        MainWindow.rd042 = MenuRD042()
        MainWindow.menu.addMenu(MainWindow.rd042)
        MainWindow.keb208 = MenuKEB208()
        MainWindow.menu.addMenu(MainWindow.keb208)

        MainWindow.main_menu.ku215.clicked.connect(lambda: MainWindow.menu.set_current(MainWindow.ku215))
        MainWindow.main_menu.rd042.clicked.connect(lambda: MainWindow.menu.set_current(MainWindow.rd042))
        MainWindow.main_menu.btp020.clicked.connect(lambda: MainWindow.menu.set_current(MainWindow.btp020))
        MainWindow.main_menu.keb208.clicked.connect(lambda: MainWindow.menu.set_current(MainWindow.keb208))
        MainWindow.ku215.onBack = lambda: MainWindow.menu.set_current(MainWindow.main_menu)

        MainWindow.menu.current = MainWindow.main_menu


class MainMenu(Menu):
    def __init__(self, parent=None, caption='Главное меню', *args):
        super().__init__(parent=parent, caption=caption, *args)
        self.ku215 = self.addMenuItem(MenuItem('Испытание крана управления КУ 215'))
        self.rd042 = self.addMenuItem(MenuItem('Испытание реле давления РД 042'))
        
        self.btp020 = MenuItem('Испытание блока тормозных приборов БТП 020')
        self.addMenuItem(self.btp020)
        self.keb208 = MenuItem('Испытание клапана электрокалибровочного КЭБ 208')
        self.addMenuItem(self.keb208)
        self.settings = MenuItem('Настройки')
        self.addMenuItem(self.settings)
        self.exit = MenuItem('Завершение работы')
        self.addMenuItem(self.exit)
        self.vbox.addStretch(1)
        self.setContentsMargins(0, 0, 0, 0)


class MenuKU215(Menu):
    def __init__(self, parent=None, caption='Испытание крана управления КУ 215', *args):
        super().__init__(parent=parent, caption=caption, *args)
        self.prepare = MenuItem('Подготовка к испытанию')
        self.addMenuItem(self.prepare)
        self.t_up = MenuItem('Проверка времени наполнения импульсной магистрали')
        self.addMenuItem(self.t_up)
        self.t_down = MenuItem('Проверка времени снижения давления в импульсной магистрали')
        self.addMenuItem(self.t_down)
        self.p_stage = MenuItem('Проверка давлений импульсной магистрали на ступенях торможения')
        self.addMenuItem(self.p_stage)
        self.p_utechka = MenuItem('Проверка величины снижения давления в импульсной'
                                  ' магистрали при создании утечки из нее')
        self.addMenuItem(self.p_utechka)
        self.germ_connection = MenuItem('Проверка плотности мест соединений')
        self.addMenuItem(self.germ_connection)
        self.germ_klap = MenuItem('Проверка плотности атмосферного клапана')
        self.addMenuItem(self.germ_klap)
        self.protokol = MenuItem('Завершение испытания')
        self.addMenuItem(self.protokol)
        self.vbox.addStretch(1)
        self.setContentsMargins(0, 0, 0, 0)


class MenuBTP020(Menu):
    def __init__(self, parent=None, caption='Испытание блока тормозных приборов БТП 020', *args):
        super().__init__(parent=parent, caption=caption, *args)
        self.prepare = MenuItem('Подготовка к испытанию')
        self.addMenuItem(self.prepare)
        self.torm_auto = MenuItem('Проверка ступенчатого торможения и отпуска при действии автоматического тормоза')
        self.addMenuItem(self.torm_auto)
        self.torm_kvt = MenuItem(
            'Проверка ступенчатого торможения и отпуска при управлении краном вспомогательного тормоза (КВТ)')
        self.addMenuItem(self.torm_kvt)
        self.t_up_kvt = MenuItem(
            'Проверка времени наполнения ТЦ при управлении краном вспомогательного тормоза (КВТ)')
        self.addMenuItem(self.t_up_kvt)
        self.germ = MenuItem('Проверка герметичности мест соединений')
        self.addMenuItem(self.germ)
        self.t_down_kvt = MenuItem('Проверка времени снижения давления в ТЦ при управлении '
                                   'краном вспомогательного тормоза (КВТ)')
        self.addMenuItem(self.t_down_kvt)
        self.bto_electr_torm = MenuItem('Проверка работы БТО при замещении электрического торможения')
        self.addMenuItem(self.bto_electr_torm)
        self.bto_high_speed = MenuItem('Проверка работы БТО при движении на повышенных скоростях')
        self.addMenuItem(self.bto_high_speed)
        self.protokol = MenuItem('Завершение испытания')
        self.addMenuItem(self.protokol)

        self.vbox.addStretch(1)
        self.setContentsMargins(0, 0, 0, 0)


class MenuRD042(Menu):
    def __init__(self, parent=None, caption='Испытание реле давления HL 042', *args):
        super().__init__(parent=parent, caption=caption, *args)
        self.prepare = MenuItem('Подготовка к испытанию')
        self.addMenuItem(self.prepare)
        self.t_up = MenuItem('Проверка времени наполнения ТЦ (торможение)')
        self.addMenuItem(self.t_up)
        self.p_const = MenuItem('Проверка автоматического поддержания установившегося зарядного\n'
                                'давления (чувствительность) в ТЦ при создании утечки из него')
        self.addMenuItem(self.p_const)
        self.t_down = MenuItem('Проверка времени снижения давления в ТЦ (отпуск)')
        self.addMenuItem(self.t_down)
        self.germ_connection = MenuItem('Проверка плотности мест соединений')
        self.addMenuItem(self.germ_connection)
        self.germ_klapan = MenuItem('Проверка плотности атмосферного клапана')
        self.addMenuItem(self.germ_klapan)
        self.protokol = MenuItem('Завершение испытания')
        self.addMenuItem(self.protokol)

        self.vbox.addStretch(1)
        self.setContentsMargins(0, 0, 0, 0)


class MenuKEB208(Menu):
    def __init__(self, parent=None, caption='Испытание клапана электроблокировочного КЭБ 208', *args):
        super().__init__(parent=parent, caption=caption, *args)
        self.prepare = MenuItem('Подготовка к испытанию')
        self.addMenuItem(self.prepare)
        self.t_up = MenuItem('Проверка времени наполнения ТЦ (торможение)')
        self.addMenuItem(self.t_up)
        self.germ = MenuItem('Проверка плотности мест соединений')
        self.addMenuItem(self.germ)
        self.t_down = MenuItem('Проверка времени снижения давления в ТЦ (отпуск)')
        self.addMenuItem(self.t_down)
        self.protokol = MenuItem('Завершение испытания')
        self.addMenuItem(self.protokol)

        self.vbox.addStretch(1)
        self.setContentsMargins(0, 0, 0, 0)
