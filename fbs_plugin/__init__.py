from mcdreforged.api.all import *
import os
import json

PLUGIN_METADATA = {
    'id': 'bot',
    'version': '1.1.0',
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

def clear_prefix(server: ServerInterface):
    global prefix
    prefix = ''
    save_prefix(server)
    server.logger.info('Prefix cleared')


#@new_thread(PLUGIN_METADATA['name'])
#def spawn_bots(source: CommandSource):
#    player = source.player
#    for i in range(1, 11):
#        source.get_server().execute(f'/execute at {player} run player {prefix}{i} spawn in survival')

@new_thread(PLUGIN_METADATA['name'])
def spawn_bots(source: CommandSource, start: int, end: int):
    player = source.player
    for i in range(start, end+1):
        source.get_server().execute(f'/execute at {player} run player {prefix}{i} spawn in survival')

@new_thread(PLUGIN_METADATA['name'])
def drop_items(source: CommandSource, start: int, end: int):
    for i in range(start, end+1):
        source.get_server().execute(f'/player {prefix}{i} dropStack all')

@new_thread(PLUGIN_METADATA['name'])
def kill_bots(source: CommandSource, start: int, end: int):
    for i in range(start, end+1):
        source.get_server().execute(f'/player {prefix}{i} kill')

def show_help_message(server: ServerInterface, info: Info):
    server.reply(info, '\n----------欢迎使用FastBotSpawn插件----------\n')
    server.reply(info, '§6!!b set bot_§r 设置前缀，§6bot_§r可随意替换，推荐和Carpet的设置一样')
    server.reply(info, '§6!!b clear§r 清除设置的前缀')
    server.reply(info, '§6!!b spawn [mini] [max]§r 批量召唤假人\n§6[mini]§r和§6[max]§r是最小和最大的序号，差值不能超过10，不写默认为1-10')
    server.reply(info, '§6!!b drop§r 召唤出的假人丢出全部物品，其余同§6spawn')
    server.reply(info, '§6!!b kill§r 批量下线假人，其余同§6spawn')

def on_user_info(server: ServerInterface, info: Info):
    global prefix
    if info.is_player:
        if info.content.startswith('!!b set'):
            prefix = info.content.split(' ')[2]
            save_prefix(server)
            server.reply(info, f'假人前缀已设置为 "{prefix}"')
        elif info.content == '!!b clear':
            clear_prefix(server)
            server.reply(info, '假人前缀已清除')
#        elif info.content == '!!b spawn':
#            spawn_bots(info)
        elif info.content.startswith('!!b spawn'):
            args = info.content.strip().split(' ')[1:]
            if len(args) == 1:
                spawn_bots(info, 1, 10)
            elif len(args) == 3:
                start = int(args[1])
                end = int(args[2])
                if end - start >= 10:
                    server.reply(info, '§c一次指令召唤数量不能大于10个，请分批执行')
                else:
                    spawn_bots(info, start, end)
#        elif info.content == '!!b drop':
#            drop_items(info)
        elif info.content.startswith('!!b drop'):
            args = info.content.strip().split(' ')[1:]
            if len(args) == 1:
                drop_items(info, 1, 10)
            elif len(args) == 3:
                start = int(args[1])
                end = int(args[2])
                drop_items(info, start, end)
#        elif info.content == '!!b kill':
#            kill_bots(info)
        elif info.content.startswith('!!b kill'):
            args = info.content.strip().split(' ')[1:]
            if len(args) == 1:
                kill_bots(info, 1, 10)
            elif len(args) == 3:
                start = int(args[1])
                end = int(args[2])
                kill_bots(info, start, end)
        elif info.content == '!!b':
            show_help_message(server, info)

def on_load(server: ServerInterface, old_module):
    load_prefix(server)
    server.register_help_message('!!b', '一键批量召唤假人')
    server.register_event_listener('minecraft.console.info', on_user_info)