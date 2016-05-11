"""
    kodiswift.listitem
    ------------------

    This module contains the ListItem class, which acts as a wrapper
    for xbmcgui.ListItem.

    :copyright: (c) 2012 by Jonathan Beluch
    :license: GPLv3, see LICENSE for more details.
"""
import warnings

from kodiswift import xbmcgui


class ListItem(object):
    """A wrapper for the xbmcgui.ListItem class. The class keeps track
    of any set properties that xbmcgui doesn't expose getters for.
    """

    def __init__(self, label=None, label2=None, icon=None, thumbnail=None,
                 path=None):
        """Defaults are an emtpy string since xbmcgui.ListItem will not
        accept None.
        """
        # kwargs = {
        #     'label': label,
        #     'label2': label2,
        #     'path': path,
        # }
        # kwargs = {k: v for k, v in kwargs.items() if v is not None}
        self._listitem = xbmcgui.ListItem(label, label2, path)

        # kodi doesn't make getters available for these properties so we'll
        # keep track on our own
        self._art = {}
        self._icon = icon
        self._path = path
        self._thumbnail = thumbnail
        self._context_menu_items = []
        self.is_folder = True
        self._played = False

    def get_context_menu_items(self):
        """Returns the list of currently set context_menu items."""
        return self._context_menu_items

    def add_context_menu_items(self, items, replace_items=False):
        """Adds context menu items. If replace_items is True all
        previous context menu items will be removed.
        """
        for label, action in items:
            assert isinstance(label, basestring)
            assert isinstance(action, basestring)
        if replace_items:
            self._context_menu_items = []
        self._context_menu_items.extend(items)
        self._listitem.addContextMenuItems(items, replace_items)

    @property
    def label(self):
        return self._listitem.getLabel()

    @label.setter
    def label(self, value):
        self._listitem.setLabel(value)

    def get_label(self):
        warnings.warn('get_label is deprecated, use label property',
                      DeprecationWarning)
        return self.label

    def set_label(self, value):
        warnings.warn('set_label is deprecated, use label property',
                      DeprecationWarning)
        return self._listitem.setLabel(value)

    @property
    def label2(self):
        return self._listitem.getLabel2()

    @label2.setter
    def label2(self, value):
        self._listitem.setLabel2(value)

    def get_label2(self):
        warnings.warn('get_label2 is deprecated, use label2 property',
                      DeprecationWarning)
        return self.label2

    def set_label2(self, value):
        warnings.warn('set_label2 is deprecated, use label2 property',
                      DeprecationWarning)
        return self._listitem.setLabel2(value)

    @property
    def selected(self):
        return self._listitem.isSelected()

    @selected.setter
    def selected(self, value):
        self._listitem.select(value)

    def is_selected(self):
        warnings.warn('is_selected is deprecated, use selected property',
                      DeprecationWarning)
        return self._listitem.isSelected()

    def select(self, selected_status=True):
        warnings.warn('select is deprecated, use selected property',
                      DeprecationWarning)
        return self._listitem.select(selected_status)

    def set_info(self, info_type, info_labels):
        """Sets the listitems info"""
        return self._listitem.setInfo(info_type, info_labels)

    def get_property(self, key):
        """Returns the property associated with the given key"""
        return self._listitem.getProperty(key)

    def set_property(self, key, value):
        """Sets a property for the given key and value"""
        return self._listitem.setProperty(key, value)

    def add_stream_info(self, stream_type, stream_values):
        """Adds stream details"""
        return self._listitem.addStreamInfo(stream_type, stream_values)

    @property
    def icon(self):
        return self._art.get('icon')

    @icon.setter
    def icon(self, value):
        self._art['icon'] = value
        self._listitem.setArt(self._art)

    def get_icon(self):
        warnings.warn('get_icon is deprecated, use icon property',
                      DeprecationWarning)
        return self._icon

    def set_icon(self, icon):
        warnings.warn('set_icon is deprecated, use icon property',
                      DeprecationWarning)
        self._icon = icon
        return self._listitem.setIconImage(icon)

    @property
    def thumbnail(self):
        return self._art.get('thumbnail')

    @thumbnail.setter
    def thumbnail(self, value):
        self._art['thumbnail'] = value
        self._listitem.setArt(self._art)

    def get_thumbnail(self):
        warnings.warn('get_thumbnail is deprecated, use thumbnail property',
                      DeprecationWarning)
        return self._thumbnail

    def set_thumbnail(self, thumbnail):
        warnings.warn('set_thumbnail is deprecated, use thumbnail property',
                      DeprecationWarning)
        self._thumbnail = thumbnail
        return self._listitem.setThumbnailImage(thumbnail)

    @property
    def path(self):
        return self._path

    @path.setter
    def path(self, value):
        self._path = value
        self._listitem.setPath(value)

    def get_path(self):
        warnings.warn('get_path is deprecated, use path property',
                      DeprecationWarning)
        return self._path

    def set_path(self, path):
        warnings.warn('set_path is deprecated, use path property',
                      DeprecationWarning)
        self._path = path
        return self._listitem.setPath(path)

    @property
    def playable(self):
        return not self.is_folder

    @playable.setter
    def playable(self, value):
        self.is_folder = not value
        is_playable = 'true' if value else 'false'
        self.set_property('isPlayable', is_playable)

    def get_is_playable(self):
        warnings.warn('get_is_playable is deprecated, use playable property',
                      DeprecationWarning)
        return not self.is_folder

    def set_is_playable(self, is_playable):
        warnings.warn('set_is_playable is deprecated, use playable property',
                      DeprecationWarning)
        value = 'false'
        if is_playable:
            value = 'true'
        self.set_property('isPlayable', value)
        self.is_folder = not is_playable

    @property
    def played(self):
        return self._played

    @played.setter
    def played(self, value):
        self._played = value

    def set_played(self, was_played):
        """Sets the played status of the listitem. Used to
        differentiate between a resolved video versus a playable item.
        Has no effect on Kodi, it is strictly used for kodiswift.
        """
        warnings.warn('set_played is deprecated, use played property',
                      DeprecationWarning)
        self._played = was_played

    def get_played(self):
        warnings.warn('get_played is deprecated, use played property',
                      DeprecationWarning)
        return self._played

    @property
    def art(self):
        return self._art

    @art.setter
    def art(self, value):
        self._art = value
        self._listitem.setArt(value)

    def set_art(self, value):
        self._art = value
        self._listitem.setArt(value)

    def as_tuple(self):
        """Returns a tuple of list item properties:
            (path, the wrapped xbmcgui.ListItem, is_folder)
        """
        return self.path, self._listitem, self.is_folder

    def as_xbmc_listitem(self):
        """Returns the wrapped xbmcgui.ListItem"""
        return self._listitem

    @classmethod
    def from_dict(cls, label=None, label2=None, icon=None, thumbnail=None,
                  path=None, selected=None, info=None, properties=None,
                  context_menu=None, replace_context_menu=False,
                  is_playable=None, info_type='video', stream_info=None):
        """A ListItem constructor for setting a lot of properties not
        available in the regular __init__ method. Useful to collect all
        the properties in a dict and then use the **dct to call this
        method.
        """
        listitem = cls(label, label2, icon, thumbnail, path)

        if selected is not None:
            listitem.select(selected)

        if info:
            listitem.set_info(info_type, info)

        if is_playable:
            listitem.set_is_playable(True)

        if properties:
            # Need to support existing tuples, but prefer to have a dict for
            # properties.
            if hasattr(properties, 'items'):
                properties = properties.items()
            for key, val in properties:
                listitem.set_property(key, val)

        if stream_info:
            for stream_type, stream_values in stream_info.items():
                listitem.add_stream_info(stream_type, stream_values)

        if context_menu:
            listitem.add_context_menu_items(context_menu, replace_context_menu)

        return listitem

    def __str__(self):
        return ('%s (%s)' % (self.label, self.path)).encode('utf-8')

    def __repr__(self):
        return ("<ListItem '%s'>" % self.label).encode('utf-8')
