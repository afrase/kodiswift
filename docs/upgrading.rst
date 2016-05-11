.. _upgrading:

Upgrading from kodiswift
========================

While the API for kodiswift is very similar to kodiswift, there are a few
backwards incompatible changes. The following list highlights the biggest
changes:

* Update all imports to use ``kodiswift`` instead of ``kodiswift``. This
  includes the dependency in your addon.xml file.

* In list item dictionaries, the ``url`` keyword has been changed to ``path``.

* In kodiswift views, the proper way to return from a view was
  ``return plugin.add_items(items)``. In kodiswift you can either ``return
  plugin.finish(items)`` or more simply ``return items``.
    .. sourcecode:: python

        # kodiswift
        return plugin.add_items(items)

        # kodiswift
        return plugin.finish(items)
        # (or)
        return items

* In the past, the ``plugin.route()`` decorator accepted arbitrary keyword
  arguments in the call to be used as defaults. These args must now be a single
  dictionary for the keyword arg ``options``.

.. sourcecode:: python

    # kodiswift
    plugin.route('/', page='1')

    # kodiswift
    plugin.route('/', options={'page': '1'})

* In list item dictionaries, the ``is_folder`` keyword is no longer necessary.
  Directory list items are the default and require no special keyword. If you
  wish to create a playable list item, set the ``is_playable`` keyword to True.
