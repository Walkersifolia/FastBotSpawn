from mcdreforged.api.all import *
import os
import json

PLUGIN_METADATA = {
    'id': 'bot',
    'version': '1.0.0',
    'name': 'FastBotSpawn',
    'description': 'A plugin with multiple functions',
    'author': 'WalkerTian',
    'link': 'https://github.com/Walkersifolia/FastBotSpawn'
}

prefix = ''
config_file = os.path.join('config', 'FastBotSpawn.json')

def save_prefix(server: ServerInterface):
    with open(config_file, 'w') as f:
        json.dump({'prefix': prefix}, f)

def load_prefix(server: ServerInterface):
    global prefix
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            data = json.load(f)
            prefix = data.get('prefix', '')

@new_thread(PLUGIN_METADATA['name'])
def drop_items(source: CommandSource):
    for i in range(1, 11):
        source.get_server().execute(f'/player {prefix}{i} dropStack all')

@new_thread(PLUGIN_METADATA['name'])
def spawn_bots(source: CommandSource):
    player = source.player
    for i in range(1, 11):
        source.get_server().execute(f'/execute at {player} run player {prefix}{i} spawn in survival')

@new_thread(PLUGIN_METADATA['name'])
def kill_bots(source: CommandSource):
    for i in range(1, 11):
        source.get_server().execute(f'/player {prefix}{i} kill')

def on_user_info(server: ServerInterface, info: Info):
    global prefix
    if info.is_player:
        if info.content.startswith('!!b set'):
            prefix = info.content.split(' ')[2]
            save_prefix(server)
            server.reply(info, f'假人前缀已设置为 "{prefix}"')
        elif info.content == '!!b drop':
            drop_items(info)
        elif info.content == '!!b spawn':
            spawn_bots(info)
        elif info.content == '!!b kill':
            kill_bots(info)

def on_load(server: ServerInterface, old_module):
    load_prefix(server)
    server.register_help_message('!!b set [prefix]', 'Set the prefix for bots')
    server.register_help_message('!!b drop', 'Drop items for players')
    server.register_help_message('!!b spawn', 'Spawn bots for players')
    server.register_help_message('!!b kill', 'Kill bots for players')
    server.register_event_listener('minecraft.console.info', on_user_info)
