import utils, settings

# Append to INSTALLED_APPS all valid plugins
mods = utils.get_valid_plugins()
for mod in mods:
    settings.INSTALLED_APPS.append('webengine.' + mod[0])
