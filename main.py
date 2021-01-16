#!/usr/bin/python3

from os import listdir, path, getenv
import re
# from steam import client as steamclient
from steam import webauth
from steamfiles import acf

modlist_id_pattern = re.compile(r'<id>steam:(\d+)</id>', re.MULTILINE)
modlist_dir_path = path.join(getenv('LOCALAPPDATA'), 'Arma 3 Launcher/Presets')
steam_install_path = 'C:/Program Files (x86)/Steam/'


def find_arma_workshop_dir():
    # Check if Arma is installed in the default library first
    # If not, we'll need to scan the other library folders for it
    if path.exists(path.join(steam_install_path, 'steamapps/appmanifest_107410.acf')):
        return path.join(steam_install_path, 'steamapps/workshop/content/107410/')

    # Make sure the libraryfolders.vdf manifest is in the usual Steam install location
    if not path.exists(path.join(steam_install_path, 'steamapps/libraryfolders.vdf')):
        raise FileNotFoundError('Unable to find Steam library folder metadata')

    # Load libraryfolders.vdf and pull out each of the library folder paths from it
    # Library paths are indexed under numeric keys that are parsed as strings, so we'll just drop the two other keys
    # and iterate over the remaining ones which will be the library paths
    with open(path.join(steam_install_path, 'steamapps/libraryfolders.vdf'), 'r') as file:
        lib_path_data = acf.load(file)
    lib_folder_paths = []
    for key in lib_path_data['LibraryFolders'].keys() - ['TimeNextStatsReport', 'ContentStatsID']:
        lib_folder_paths.append(path.join(lib_path_data['LibraryFolders'][key]))

    # Look in each of the library paths for the Arma 3 app manifest file
    for lib_folder_path in lib_folder_paths:
        if path.exists(path.join(lib_folder_path, 'steamapps/appmanifest_107410.acf')):
            return path.join(lib_folder_path, 'steamapps/workshop/content/107410/')

    return None


if __name__ == '__main__':
    _mod_dir_path = find_arma_workshop_dir()
    if not _mod_dir_path:
        raise FileNotFoundError('Unable to find Arma 3 install location')

    # Collect modlists
    modlist_paths = [path.join(modlist_dir_path, filename) for filename in listdir(modlist_dir_path) if filename.lower().endswith('.preset2')]

    # Parse IDs and collect them into a set
    mod_ids = set()
    for modlist_path in modlist_paths:
        with open(modlist_path, 'r') as file:
            content = str.join('', file.readlines())
        for id in modlist_id_pattern.findall(content):
            mod_ids.add(id)
    print(str.format('Found {} mods installed across {} modlists', len(mod_ids), len(modlist_paths)))

    # Collect installed mod IDs (excluding missions)
    # Addons should always have a meta.cpp file in their root
    installed_mod_ids = set([dir for dir in listdir(_mod_dir_path) if 'meta.cpp' in listdir(path.join(_mod_dir_path, dir))])
    print(str.format('Found {} mods currently installed', len(installed_mod_ids)))

    # Subtract the mod IDs in the modlists from those installed to get the redundant ones we need to remove
    mod_ids_to_unsub = installed_mod_ids - mod_ids
    print(str.format('Removing {} redundant mods not included in any modlist', len(mod_ids_to_unsub)))

    # Interface with the Steam client and create a web client
    # steam_client = steamclient.SteamClient()
    # steam_client.cli_login()
    # steam_web = steam_client.get_web_session()
    # OR...
    steam_auth = webauth.WebAuth(input('Steam username: '))
    steam_web = steam_auth.cli_login()

    # Unsub from the redundant mods
    unsubbed_mod_ids = set()
    index = 0
    for id in mod_ids_to_unsub:
        index += 1
        print(str.format('[{}/{}] Unsubscribing from {}...', index, len(mod_ids_to_unsub), id), end=' ')
        res = steam_web.post('https://steamcommunity.com/sharedfiles/unsubscribe', {'appid': '107410', 'id': id, 'sessionid': steam_auth.session_id})
        if res.status_code == 200:
            unsubbed_mod_ids.add(id)
            print('Success')
        else:
            print('Failed')

    # Report what was unsubbed
    print('Successfully unsubscribed from the following mods:')
    for id in unsubbed_mod_ids:
        print('https://steamcommunity.com/sharedfiles/filedetails/?id=' + str(id))
