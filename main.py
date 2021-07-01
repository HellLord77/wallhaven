# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.9 (tags/v3.8.9:a743f81, Apr  2 2021, 10:59:45) [MSC v.1928 32 bit (Intel)]
# Embedded file name: wallhaven.py
import ctypes
import os
import random
import sys
import threading
import winreg

import requests
import wx
import wx.adv
import wx.lib.embeddedimage

import singleton

singleton.init(crash_handler=print, crash_handler_args=('[#] Crash',), exit_handler=print,
               exit_handler_args=('[#] Exit',))
MAX_PATH = 260
SPI_GETDESKWALLPAPER = 115
SPI_SETDESKWALLPAPER = 20
SPIF_SENDWININICHANGE = 2
DEFAULT_FRAME_STYLE = wx.CAPTION | wx.CLOSE_BOX | wx.STAY_ON_TOP | wx.FRAME_TOOL_WINDOW
NAME = 'wallhaven'
ICON = wx.lib.embeddedimage.PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABHNCSVQICAgIfAhkiAAAAnhJREFUOI11k79KXEEUxr/5c+/evenEQhA0gooYOxvRxQfwFSLBQrAJeQFBYmNrSLBb8SmyInYWCcg2uqYJiZXg3SYr7t7d+X9SXO+NCWTgMAdmvt+Z+c4Mu729fROCe2eMWyKimHPOAIAxhn8HEeFpzTImbuJYfmTfbm7aURTNJ/X6iyRJOOcCAFWAYiYQoQgEaKVpNBzm2pjvcqTUUlKvR0IIHkIAUSEuo6xKREVOBM45k1GU9vv9V9w5F0spORGhBPwvjDF4v7+PnZ0dSCm58z6WgQIjCvD+z105FygtKE9BIBwcHOD15iamp6bgvQcRMe6dh3MeIQSEEGCMQav1GScnJ2g0Guh2uwCAr1++YjAY4OX0dLXX+wBeJL46/uHhIWZmZrC6uoqFhQVMTEyAMYbT01Osra2hvGqhc+DOuQoQQkCr1cLc3Bza7TaWl5chhADnHJeXl1hZWakApUaWAM45GGNYX19HCAHn5+eYnJxEs9lEnudIkgTj4+Ow1lYA5xxkmZRt293dhXMO9/f3aDabqNVqODs7Q5Zl8N5XwrKwdNbBWvvkf2F9u91Go9EAgaC1xtXVFRYXF2GtrcTOFTqujYYxBsYYWGuQ5zmur6+xvb0NrTS01uh0Opidna32PQ9ujIFSCt1uF1tbW9jb28PGxgY451BKYTQa4e7uDkdHR7i4uIDWBVQpBWst2PHxsRkbG5NpmrI4jhFFEaSUEEJUvgCojLPWwliDfJBTr/fgZK/3q0PAvPc+TdOUO+cghPgLUD7lEjAcDunx8XH48PDwQ2ZZ95NS+u1oOFqq1aJYyohJKau2Pv/KZResta7f7//MsuzDb1Mp5IMPSMlnAAAAAElFTkSuQmCC')
URL = 'https://wallhaven.cc/api/v1/'
APPDATA_PATH = os.environ['APPDATA']
CACHEDFILES_PATH = os.path.join(APPDATA_PATH, 'Microsoft', 'Windows', 'Themes', 'CachedFiles')
CONFIG_PATH = os.path.join(APPDATA_PATH, '{}.ini'.format(NAME))
PICTURES_PATH = os.path.join(os.environ['USERPROFILE'], 'Pictures', NAME)
TEMP_PATH = os.path.join(os.environ['TEMP'], NAME)
configs = {'auto_change': False,
           'change_interval': 3600000,
           'auto_save': False,
           'save_path': PICTURES_PATH,
           'use_api_key': True,
           'auto_ratio': True,
           'auto_startup': False}
interval = {'300000': '5 Minute',
            '900000': '15 Minute',
            '1800000': '30 Minute',
            '3600000': '1 Hour',
            '10800000': '3 Hour',
            '21600000': '6 Hour'}
params = {'apikey': None,
          'q': None,
          'categories': '111',
          'purity': '100',
          'sorting': 'date_added',
          'order': 'desc',
          'topRange': '1M',
          'atleast': None,
          'resolutions': None,
          'ratios': None,
          'colors': None,
          'page': None,
          'seed': None}
categories = {'0': 'General',
              '1': 'Anime',
              '2': 'People'}
purity = {'0': 'SFW',
          '1': 'Sketchy',
          '2': 'NSFW'}
sorting = {'date_added': 'Date Added',
           'relevance': 'Relevance',
           'random': 'Random',
           'views': 'Views',
           'favorites': 'Favorites',
           'toplist': 'Toplist',
           'toplist-beta': 'Toplist Beta'}
order = {'desc': 'Descending',
         'asc': 'Ascending'}
topRange = {'1d': 'Last Day',
            '3d': 'Last 3 Days',
            '1w': 'Last Week',
            '1M': 'Last Month',
            '3M': 'Last 3 Months',
            '6M': 'Last 6 Months',
            '1y': 'Last Year'}
atleast = [
    'None',
    '_5:4', '1280x1024', '1600x1280', '1920x1536', '2560x2048', '3840x3072',
    '_4:3', '1280x960', '1600x1200', '1920x1440', '2560x1920', '3840x2880',
    '_16:10', '1280x800', '1600x1000', '1920x1200', '2560x1600', '3840x2400',
    '_16:9', '1280x720', '1600x900', '1920x1080', '2560x1440', '3840x2160',
    '_Ultrawide', '2560x1080', '3440x1440', '3840x1600']
atleast = {resolution: resolution for resolution in atleast}
resolutions = dict(atleast)
del resolutions['None']
ratios = [
    '_Square', '1x1', '3x2', '4x3', '5x4',
    '_Portrait', '9x16', '10x16', '9x18',
    '_Ultrawide', '21x9', '32x9', '48x9',
    '_Wide', '16x9', '16x10']
ratios = {ratio: ratio for ratio in ratios}
colors = [
    'None',
    '#660000', '#990000', '#cc0000', '#cc3333', '#ea4c88',
    '#993399', '#663399', '#333399', '#0066cc', '#0099cc',
    '#66cccc', '#77cc33', '#669900', '#336600', '#666600',
    '#999900', '#cccc33', '#ffff00', '#ffcc33', '#ff9900',
    '#ff6600', '#cc6633', '#996633', '#663300', '#000000',
    '#999999', '#cccccc', '#ffffff', '#424153']
colors = {color: color for color in colors}


def create_item(menu, label, func):
    item = wx.MenuItem(menu, wx.ID_ANY, label)
    menu.Bind((wx.EVT_MENU), func, id=(item.GetId()))
    menu.Append(item)
    return item


def create_submenu_items(item_submenu, dict_, kind):
    submenu = item_submenu.GetSubMenu()
    if kind == wx.ITEM_RADIO:
        append_checkable = submenu.AppendRadioItem
    else:
        append_checkable = submenu.AppendCheckItem
    for id, label in dict_.items():
        kind = id[0]
        if kind == '_':
            submenu_item = append_checkable(wx.ID_ANY, label[1:])
            submenu_item.Enable(False)
        elif kind == '#':
            item_color = wx.Colour()
            item_color.Set(id)
            submenu_item = wx.MenuItem(submenu, wx.ID_ANY, label, id, wx.ITEM_RADIO)
            submenu_item.SetBackgroundColour(item_color)
            submenu.Append(submenu_item)
        else:
            append_checkable(wx.ID_ANY, label, id)


def get_param_submenu_items_id(item_submenu):
    id = item_submenu.GetHelp()
    param = params[id]
    submenu = item_submenu.GetSubMenu()
    submenu_items = submenu.GetMenuItems()
    return (param, submenu_items, id)


def parse_params_1(item_submenu):
    param, submenu_items = get_param_submenu_items_id(item_submenu)[:-1]
    for index, state in enumerate(param):
        submenu_items[index].Check(int(state))


def parse_params_2(item_submenu):
    param, submenu_items = get_param_submenu_items_id(item_submenu)[:-1]
    for submenu_item in submenu_items:
        if submenu_item.GetHelp() == param:
            submenu_item.Check(True)
            break


def parse_params_3(item_submenu):
    param, submenu_items = get_param_submenu_items_id(item_submenu)[:-1]
    for submenu_item in submenu_items:
        id = submenu_item.GetHelp()
        state = id in param if (id and param) else False
        submenu_item.Check(state)


def update_params_1(item_submenu):
    param = ''
    submenu_items, id = get_param_submenu_items_id(item_submenu)[1:]
    for submenu_item in submenu_items:
        state = submenu_item.IsChecked()
        param += str(int(state))
    else:
        params[id] = param


def update_params_2(item_submenu):
    submenu_items, id = get_param_submenu_items_id(item_submenu)[1:]
    for submenu_item in submenu_items:
        if submenu_item.IsChecked():
            param = submenu_item.GetHelp()
            param = param.replace('#', '')
            params[id] = None if param == 'None' else param
            break


def update_params_3(item_submenu):
    submenu_items, id = get_param_submenu_items_id(item_submenu)[1:]
    for submenu_item in submenu_items:
        param = ''
        if submenu_item.IsChecked():
            dim = submenu_item.GetHelp()
            param += '{},'.format(dim)
        param = param or None
        params[id] = param


def modify_search_query(textctrl, loop):
    search_query = textctrl.GetLineText(0)
    params['q'] = search_query or None
    loop.Exit()


def verify_api_key(api_key):
    url = os.path.join(URL, 'settings')
    response = requests.get(url=url, params={'apikey': api_key})
    return response.status_code


def get_ratio():
    display_resolution = wx.DisplaySize()
    display_ratio = display_resolution[0] / display_resolution[1]
    for ratio in ratios:
        if ratio[0] != '_':
            w, h = ratio.split('x')
            aspect_ratio = int(w) / int(h)
            d1 = abs(display_ratio - aspect_ratio)
            try:
                if d1 <= d0:
                    d0 = d1
                    optimal_ratio = ratio
            except UnboundLocalError:
                d0 = d1

    return optimal_ratio


def on_modify_search_query(_):
    def func(_):
        return modify_search_query(textctrl, loop)

    frame = wx.Frame(None, (wx.ID_ANY), 'Search Query', style=DEFAULT_FRAME_STYLE)
    frame.Bind(wx.EVT_CLOSE, lambda _: loop.Exit())
    panel = wx.Panel(frame, wx.ID_ANY)
    staticbox = wx.StaticBox(panel, wx.ID_ANY, 'Current Search Query: {}'.format(params['q']))
    sizer = wx.StaticBoxSizer(staticbox)
    textctrl = wx.TextCtrl(panel, (wx.ID_ANY), (params['q'] or ''), style=(wx.TE_PROCESS_ENTER))
    textctrl.Bind(wx.EVT_TEXT_ENTER, func)
    sizer.Add(textctrl, wx.EXPAND)
    button = wx.Button(panel, wx.ID_ANY, 'Modify Search Query')
    button.Bind(wx.EVT_BUTTON, func)
    sizer.Add(button)
    panel.SetSizer(sizer)
    sizer.SetSizeHints(frame)
    show_frame(frame)
    button.SetDefault()
    loop = wx.GUIEventLoop()
    loop.Run()
    frame.Destroy()


def show_frame(frame):
    w0, h0 = wx.ClientDisplayRect()[2:]
    w, h = frame.GetSize()
    frame.SetPosition((w0 - w, h0 - h))
    frame.Show()
    frame.Raise()


def remove_temp():
    if os.path.isdir(TEMP_PATH):
        temp_files = os.listdir(TEMP_PATH)
        for temp_file in temp_files:
            temp_file_path = os.path.join(TEMP_PATH, temp_file)
            os.remove(temp_file_path)
        else:
            os.rmdir(TEMP_PATH)


class TaskBarIcon(wx.adv.TaskBarIcon):

    def __init__(self):
        super().__init__()
        self.icon = ICON.GetIcon()
        self.SetIcon(self.icon, NAME)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.on_change)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_DOWN, self.on_right_down)
        app.Bind(wx.EVT_END_SESSION, self.on_exit)
        self.config = Config(CONFIG_PATH, configs, params)
        self.config.load()
        self.save_path = configs['save_path']
        self.change_interval = configs['change_interval']
        self.bk_categories = params['categories']
        self.bk_purity = params['purity']
        self.bk_atleast_1 = self.bk_atleast_2 = params['atleast']
        self.bk_resolutions_1 = self.bk_resolutions_2 = params['resolutions']
        self.bk_ratios = params['ratios']
        self.bk_search_params = {}
        self.search_data = []
        self.search = None
        self.func_progress = lambda progress: self.change_wallpaper.SetItemLabel(
            'Change Wallpaper ({:03}%)'.format(progress))
        self.thread = threading.Thread(target=(self.change))
        self.display_ratio = get_ratio()
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.on_change, self.timer)
        self.menu = wx.Menu()
        self.change_wallpaper = create_item(self.menu, 'Change Wallpaper', self.on_change)
        self.auto_change = self.menu.AppendCheckItem(wx.ID_ANY, 'Auto Change Wallpaper')
        self.auto_change.Check(configs['auto_change'])
        self.menu.Bind((wx.EVT_MENU), (self.on_auto_change), id=(self.auto_change.GetId()))
        self.item_submenu_interval = self.menu.AppendSubMenu(wx.Menu(), 'Auto Change Interval')
        create_submenu_items(self.item_submenu_interval, interval, wx.ITEM_RADIO)
        self.menu.AppendSeparator()
        self.save_wallpaper = create_item(self.menu, 'Save Wallpaper', self.on_save)
        self.auto_save = self.menu.AppendCheckItem(wx.ID_ANY, 'Auto Save Wallpaper')
        self.auto_save.Check(configs['auto_save'])
        create_item(self.menu, 'Modify Save Folder', self.on_modify_save_folder)
        self.menu.AppendSeparator()
        self.use_api_key = self.menu.AppendCheckItem(wx.ID_ANY, 'Use API Key')
        self.use_api_key.Check(bool(configs['use_api_key'] and params['apikey']))
        create_item(self.menu, 'Modify API Key', self.on_modify_api_key)
        self.remove_api_key = create_item(self.menu, 'Remove API Key', self.on_remove_api_key)
        self.remove_api_key.Enable(bool(params['apikey']))
        self.menu.AppendSeparator()
        create_item(self.menu, 'Modify Search Query', on_modify_search_query)
        self.item_submenu_categories = self.menu.AppendSubMenu(wx.Menu(), 'Category', 'categories')
        create_submenu_items(self.item_submenu_categories, categories, wx.ITEM_CHECK)
        self.item_submenu_purity = self.menu.AppendSubMenu(wx.Menu(), 'Purity', 'purity')
        create_submenu_items(self.item_submenu_purity, purity, wx.ITEM_CHECK)
        self.item_submenu_colors = self.menu.AppendSubMenu(wx.Menu(), 'Color', 'colors')
        create_submenu_items(self.item_submenu_colors, colors, wx.ITEM_RADIO)
        self.menu.AppendSeparator()
        self.item_submenu_sorting = self.menu.AppendSubMenu(wx.Menu(), 'Sort By', 'sorting')
        create_submenu_items(self.item_submenu_sorting, sorting, wx.ITEM_RADIO)
        self.item_submenu_order = self.menu.AppendSubMenu(wx.Menu(), 'Sort Order', 'order')
        create_submenu_items(self.item_submenu_order, order, wx.ITEM_RADIO)
        self.item_submenu_topRange = self.menu.AppendSubMenu(wx.Menu(), 'Top List Range', 'topRange')
        create_submenu_items(self.item_submenu_topRange, topRange, wx.ITEM_RADIO)
        self.menu.AppendSeparator()
        self.auto_ratio = self.menu.AppendCheckItem(wx.ID_ANY, 'Auto Ratio ({})'.format(self.display_ratio))
        self.auto_ratio.Check(configs['auto_ratio'])
        self.menu.Bind((wx.EVT_MENU), (self.on_auto_ratio), id=(self.auto_ratio.GetId()))
        self.item_submenu_ratios = self.menu.AppendSubMenu(wx.Menu(), 'Resolution Ratio', 'ratios')
        create_submenu_items(self.item_submenu_ratios, ratios, wx.ITEM_CHECK)
        self.item_submenu_atleast = self.menu.AppendSubMenu(wx.Menu(), 'Least Resolution', 'atleast')
        create_submenu_items(self.item_submenu_atleast, atleast, wx.ITEM_RADIO)
        self.item_submenu_resolutions = self.menu.AppendSubMenu(wx.Menu(), 'Exact Resolution', 'resolutions')
        create_submenu_items(self.item_submenu_resolutions, resolutions, wx.ITEM_CHECK)
        self.menu.AppendSeparator()
        self.auto_startup = self.menu.AppendCheckItem(wx.ID_ANY, 'Auto Startup')
        self.auto_startup.Check(configs['auto_startup'])
        self.save_configuration = self.menu.AppendCheckItem(wx.ID_ANY, 'Save Configuration')
        self.save_configuration.Check(self.config.exists)
        self.menu.Bind((wx.EVT_MENU), (self.on_auto_startup), id=(self.auto_startup.GetId()))
        create_item(self.menu, 'Exit Wallhaven', self.on_exit)
        self.parse_interval()
        self.parse_params()
        self.update_popup_menu()
        self.on_auto_change()
        self.on_auto_ratio()
        self.on_auto_startup()
        self.on_change() if sys.argv[(-1)] == '-c' else None

    def update_popup_menu(self):
        if params['apikey']:
            self.use_api_key.Enable(True)
        else:
            self.use_api_key.Enable(False)
            self.use_api_key.Check(False)
        nsfw = self.item_submenu_purity.GetSubMenu().GetMenuItems()[(-1)]
        if self.use_api_key.IsChecked():
            nsfw.Enable(True)
        else:
            nsfw.Enable(False)
            nsfw.Check(False)
        submenu_sorting = self.item_submenu_sorting.GetSubMenu()
        state_1 = submenu_sorting.FindItemById(submenu_sorting.FindItem('Toplist')).IsChecked()
        state_2 = submenu_sorting.FindItemById(submenu_sorting.FindItem('Toplist Beta')).IsChecked()
        self.item_submenu_topRange.Enable(state_1 or state_2)
        atleast = params['atleast']
        if self.bk_atleast_1 != atleast:
            if atleast:
                params['resolutions'] = None
                parse_params_3(self.item_submenu_resolutions)
        elif self.bk_resolutions_1 != params['resolutions']:
            params['atleast'] = 'None'
            parse_params_2(self.item_submenu_atleast)

    def parse_interval(self):
        submenu_interval = self.item_submenu_interval.GetSubMenu()
        intervals = submenu_interval.GetMenuItems()
        for interval in intervals:
            if int(interval.GetHelp()) == self.change_interval:
                interval.Check(True)
                break

    def update_interval(self):
        submenu_interval = self.item_submenu_interval.GetSubMenu()
        intervals = submenu_interval.GetMenuItems()
        for interval in intervals:
            if interval.IsChecked():
                change_interval = int(interval.GetHelp())
                restart = self.change_interval != change_interval
                self.change_interval = change_interval
                self.on_auto_change() if restart else None
                break

    def parse_params(self):
        parse_params_1(self.item_submenu_categories)
        parse_params_1(self.item_submenu_purity)
        parse_params_2(self.item_submenu_sorting)
        parse_params_2(self.item_submenu_order)
        parse_params_2(self.item_submenu_topRange)
        parse_params_2(self.item_submenu_atleast)
        parse_params_3(self.item_submenu_resolutions)
        parse_params_3(self.item_submenu_ratios)
        parse_params_2(self.item_submenu_colors)

    def update_params(self):
        update_params_1(self.item_submenu_categories)
        update_params_1(self.item_submenu_purity)
        update_params_2(self.item_submenu_sorting)
        update_params_2(self.item_submenu_order)
        update_params_2(self.item_submenu_topRange)
        update_params_2(self.item_submenu_atleast)
        update_params_3(self.item_submenu_resolutions)
        update_params_3(self.item_submenu_ratios)
        update_params_2(self.item_submenu_colors)

    def fix_categories_purity(self):
        if not int(params['categories']):
            params['categories'] = self.bk_categories
            parse_params_1(self.item_submenu_categories)
        if not int(params['purity']):
            params['purity'] = self.bk_purity
            parse_params_1(self.item_submenu_purity)

    def on_right_down(self, _):
        self.bk_atleast_1 = params['atleast']
        self.bk_resolutions_1 = params['resolutions']
        self.PopupMenu(self.menu)
        self.update_interval()
        self.update_params()
        self.update_popup_menu()

    def on_change(self, _=None):
        if not self.thread.is_alive():
            self.thread.start()
            self.thread = threading.Thread(target=(self.change))

    def on_auto_change(self, _=None):
        state = self.auto_change.IsChecked()
        self.item_submenu_interval.Enable(state)
        self.timer.Start(self.change_interval) if state else self.timer.Stop()
        self.on_auto_startup() if self.auto_startup.IsChecked() else None

    def on_save(self, _):
        self.save_wallpaper.Enable(False)
        wallpaper_path = ctypes.create_unicode_buffer(MAX_PATH)
        ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, MAX_PATH, ctypes.byref(wallpaper_path), None)
        wallpaper_name = os.path.basename(wallpaper_path.value)
        path = os.path.join(CACHEDFILES_PATH, os.listdir(CACHEDFILES_PATH)[0])
        wallpaper = Wallpaper(path, None, CACHEDFILES_PATH, self.save_path, wallpaper_name)
        wallpaper.save()
        self.save_wallpaper.Enable(True)

    def on_modify_save_folder(self, _=None):
        save_path = self.save_path
        while not os.path.isdir(save_path):
            if save_path:
                save_path = os.path.dirname(save_path)

        frame = wx.Frame(None, (wx.ID_ANY), 'Save Folder', style=DEFAULT_FRAME_STYLE)
        frame.Bind(wx.EVT_CLOSE, lambda _: loop.Exit())
        panel = wx.Panel(frame, wx.ID_ANY)
        staticbox = wx.StaticBox(panel, wx.ID_ANY, 'Current Save Folder: {}'.format(self.save_path))
        sizer = wx.StaticBoxSizer(staticbox)
        dirpickerctrl = wx.DirPickerCtrl(panel, wx.ID_ANY, save_path, 'Browse for Folder')
        sizer.Add(dirpickerctrl, wx.EXPAND)
        button = wx.Button(panel, wx.ID_ANY, 'Modify Save Folder')
        button.Bind(wx.EVT_BUTTON, lambda _: self.modify_save_folder(dirpickerctrl, loop))
        sizer.Add(button)
        panel.SetSizer(sizer)
        sizer.SetSizeHints(frame)
        show_frame(frame)
        button.SetDefault()
        loop = wx.GUIEventLoop()
        loop.Run()
        frame.Destroy()

    def on_modify_api_key(self, _):
        frame = wx.Frame(None, (wx.ID_ANY), 'API Key', style=DEFAULT_FRAME_STYLE)
        frame.Bind(wx.EVT_CLOSE, lambda _: loop.Exit())
        frame.CreateStatusBar()
        frame.SetStatusText('[#] Get API Key from https://wallhaven.cc/settings/account')
        panel = wx.Panel(frame, wx.ID_ANY)
        staticbox = wx.StaticBox(panel, wx.ID_ANY, 'Current API Key: {}'.format(params['apikey']))
        sizer = wx.StaticBoxSizer(staticbox)
        button = wx.Button(panel, wx.ID_ANY, 'Fetch API Key From Clipboard && Modify API Key After Verifying')
        button.Bind(wx.EVT_BUTTON, lambda _: self.modify_api_key(frame, button, loop))
        sizer.Add(button)
        panel.SetSizer(sizer)
        sizer.SetSizeHints(frame)
        show_frame(frame)
        loop = wx.GUIEventLoop()
        loop.Run()
        frame.Destroy()

    def on_remove_api_key(self, _):
        params['apikey'] = None
        self.remove_api_key.Enable(False)

    def on_auto_ratio(self, _=None):
        state = self.auto_ratio.IsChecked()
        enable = not state
        self.item_submenu_atleast.Enable(enable)
        self.item_submenu_resolutions.Enable(enable)
        self.item_submenu_ratios.Enable(enable)
        if state:
            self.bk_atleast_2 = params['atleast']
            self.bk_resolutions_2 = params['resolutions']
            self.bk_ratios = params['ratios']
            params['atleast'] = 'None'
            params['resolutions'] = None
            params['ratios'] = '{},'.format(self.display_ratio)
        else:
            params['atleast'] = self.bk_atleast_2
            params['resolutions'] = self.bk_resolutions_2
            params['ratios'] = self.bk_ratios
        parse_params_2(self.item_submenu_atleast)
        parse_params_3(self.item_submenu_resolutions)
        parse_params_3(self.item_submenu_ratios)
        update_params_2(self.item_submenu_atleast)

    def on_auto_startup(self, _=None):
        key = 'wallhaven'
        path = os.path.realpath(sys.argv[0])
        value = '"{}" -c'.format(path) if self.auto_change.IsChecked() else '"{}"'.format(path)
        sub_key = 'Software\\Microsoft\\Windows\\CurrentVersion\\Run'
        handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key, 0, winreg.KEY_SET_VALUE)
        if self.auto_startup.IsChecked():
            try:
                winreg.SetValueEx(handle, key, 0, winreg.REG_SZ, value)
            except PermissionError:
                self.auto_startup.Check(False)

        else:
            try:
                winreg.DeleteValue(handle, key)
            except FileNotFoundError:
                pass

    def on_exit(self, _):
        self.save_config() if self.save_configuration.IsChecked() else os.remove(CONFIG_PATH) if os.path.isfile(
            CONFIG_PATH) else None
        remove_temp()
        wx.CallAfter(self.Destroy)

    def change(self):
        self.change_wallpaper.Enable(False)
        self.change_wallpaper.SetItemLabel('Change Wallpaper (000%)')
        self.fix_categories_purity()
        search_params = dict(params)
        search_params['apikey'] = search_params['apikey'] if self.use_api_key.IsChecked() else None
        if self.bk_search_params != search_params:
            self.search = Search(search_params)
            self.search_data = []
        if not self.search_data:
            self.search_data = self.search.get()
            random.shuffle(self.search_data)
        if self.search_data:
            wallpaper_data = self.search_data.pop()
            wallpaper_path = wallpaper_data['path']
            wallpaper_file_size = wallpaper_data['file_size']
            wallpaper = Wallpaper(wallpaper_path, wallpaper_file_size, TEMP_PATH, self.save_path, None,
                                  self.func_progress)
            wallpaper.get()
            wallpaper.set()
            wallpaper.save() if self.auto_save.IsChecked() else None
        self.bk_search_params = dict(search_params)
        self.change_wallpaper.SetItemLabel('Change Wallpaper')
        self.change_wallpaper.Enable(True)

    def modify_save_folder(self, dirpickerctrl, loop):
        save_path = dirpickerctrl.GetPath()
        while not os.path.isdir(save_path):
            if save_path:
                save_path = os.path.dirname(save_path)

        if save_path:
            self.save_path = save_path
            loop.Exit()

    def modify_api_key(self, frame, button, loop):
        button.Disable()
        frame.Update()
        frame.SetStatusText('[#] Verifying API Key')
        text_data = wx.TextDataObject()
        wx.TheClipboard.GetData(text_data)
        api_key = text_data.GetText()
        status_code = verify_api_key(api_key)
        if status_code == 200:
            params['apikey'] = api_key
            self.remove_api_key.Enable(True)
            loop.Exit()
        else:
            frame.SetStatusText('[#] Invalid API Key ({})'.format(requests.status_codes._codes[status_code][0]))
            app.Yield()
            button.Enable()
            button.SetFocus()

    def save_config(self):
        configs.update({'auto_change': self.auto_change.IsChecked(),
                        'change_interval': self.change_interval,
                        'auto_save': self.auto_save.IsChecked(),
                        'save_path': self.save_path,
                        'use_api_key': self.use_api_key.IsChecked(),
                        'auto_ratio': self.auto_ratio.IsChecked(),
                        'auto_startup': self.auto_startup.IsChecked()})
        self.config.save()


class Config:
    import pickle

    def __init__(self, path, *config):
        self.path = path
        self.config = config
        self.exists = self._exists()

    def _exists(self):
        return os.path.isfile(CONFIG_PATH)

    def get(self):
        config = self.config
        if self.exists:
            with open(self.path, 'rb') as (file):
                pickled = file.read()
            try:
                config = self.pickle.loads(pickled)
            except self.pickle.UnpicklingError:
                print('[#] UnpicklingError')

        return config

    def load(self):
        config = self.get()
        zipped = zip(self.config, config)
        [current.update(saved) for current, saved in zipped]

    def save(self):
        pickled = self.pickle.dumps(self.config)
        with open(self.path, 'wb') as (file):
            file.write(pickled)


class Search:

    def __init__(self, params):
        self.url = os.path.join(URL, 'search')
        self.params = dict(params)
        self.page = 1
        self.last_page = 1
        self.seed = None
        self.meta = None

    def get(self):
        data = []
        try:
            response = requests.get(url=(self.url), params=(self.params))
            status_code = response.status_code
            if status_code == 200:
                data, self.meta = response.json().values()
                self.set()
        except requests.exceptions.ConnectionError:
            status_code = 418
        else:
            print('[#] {}'.format(requests.status_codes._codes[status_code][0]))
            return data

    def set(self):
        if self.page == 1:
            self.last_page = self.meta['last_page']
            self.seed = self.meta['seed']
        self.page = self.page % self.last_page + 1
        self.params['page'] = self.page
        self.params['seed'] = self.seed


class Wallpaper:
    buffer = 1

    def __init__(self, path, file_size, temp_path, save_path, file_name=None, callback=None):
        self.temp_path = os.path.join(temp_path, os.path.basename(path))
        self.save_path = os.path.join(save_path, file_name or os.path.basename(path))
        self.save_dir = save_path
        self.file_size = file_size
        self.response = requests.get(path, stream=True) if self.file_size else None
        self.callback = callback

    def get(self):
        if os.path.isfile(self.temp_path) or os.path.isfile(self.save_path):
            return
        temp_dir = os.path.dirname(self.temp_path)
        os.makedirs(temp_dir, exist_ok=True)
        downloaded = progress = 0
        chunk_size = self.file_size // 100 * self.buffer
        iter_content = self.response.iter_content(chunk_size)
        with open(self.temp_path, 'wb') as (cache_file):
            for chunk in iter_content:
                cache_file.write(chunk)
                progress += self.buffer if progress < 100 else 0
                self.callback(progress) if self.callback else None
                downloaded += len(chunk)
                print(('[{}] {}'.format(str('#' * progress).ljust(100), downloaded)), end='\r')

        print()

    def save(self):
        if os.path.isfile(self.temp_path):
            if not os.path.isfile(self.save_path):
                with open(self.temp_path, 'rb') as (cache_file):
                    data = cache_file.read()
                save_dir = os.path.dirname(self.save_path)
                os.makedirs(save_dir, exist_ok=True)
                with open(self.save_path, 'wb') as (save_file):
                    save_file.write(data)

    def set(self):
        if os.path.isfile(self.temp_path):
            path = self.temp_path
        else:
            if os.path.isfile(self.save_path):
                path = self.save_path
            else:
                return
        ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, None, path, SPIF_SENDWININICHANGE)


if __name__ == '__main__':
    app = wx.App()
    TaskBarIcon()
    app.MainLoop()
    sys.exit()
