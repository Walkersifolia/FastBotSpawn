from mcdreforged.api.all import *
import os
import json

PLUGIN_METADATA = {
    'id': 'bot',
    'version': '1.1.1',
    'name': 'FastBotSpawn',
    'description': 'A plugin with multiple functions',
    'author': 'WalkerTian',
    'link': 'https://github.com/Walkersifolia/FastBotSpawn'
}

prefix = ''
limit = 10
config_file = os.path.join('config', 'FastBotSpawn.json')

def save_config(server: ServerInterface):
    with open(config_file, 'w') as f:
        json.dump({'prefix': prefix, 'limit': limit}, f)

def load_config(server: ServerInterface):
    global prefix, limit
    if os.path.exists(config_file):
        with open(config_file, 'r') as f:
            data = json.load(f)
            prefix = data.get('prefix', '')
            limit = data.get('limit', 10)

def clear_prefix(server: ServerInterface):
    global prefix
    prefix = ''
    save_config(server)
    server.logger.info('Prefix cleared')

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
    server.reply(info, '§6!!b set bot_§r 设置前缀，§6bot_§r可替换，推荐和Carpet配置同步，没有就留空')
    server.reply(info, '§6!!b limit [number]§r 设置最大生成数量，默认为10')
    server.reply(info, '§6!!b clear§r 清除设置的前缀')
    server.reply(info, '§6!!b spawn [mini] [max]§r 批量召唤假人')
    server.reply(info, '§6!!b drop [mini] [max]§r 批量控制假人丢出全部物品')
    server.reply(info, '§6!!b kill [mini] [max]§r 批量下线假人')
    server.reply(info, '§6[mini]§r和§6[max]§r是最小和最大的序号，差值不能超过10，不写默认为1-10')

def on_user_info(server: ServerInterface, info: Info):
    global prefix, limit
    if info.is_player:
        if info.content.startswith('!!b set'):
            prefix = info.content.split(' ')[2]
            save_config(server)
            server.reply(info, f'假人前缀已设置为 "{prefix}"')
        elif info.content == '!!b clear':
            clear_prefix(server)
            server.reply(info, '假人前缀已清除')
        elif info.content.startswith('!!b limit'):
            limit = info.content.split(' ')[2]
            save_config(server)
            server.reply(info, f'假人单次召唤上限已设置为{limit}')
        elif info.content.startswith('!!b spawn'):
            args = info.content.strip().split(' ')[1:]
            if len(args) == 1:
                spawn_bots(info, 1, 10)
            elif len(args) == 3:
                start = int(args[1])
                end = int(args[2])
                if end - start >= int(limit):
                    server.reply(info, f'§c一次指令召唤数量不能大于{limit}个，请分批执行')
                else:
                    spawn_bots(info, start, end)
        elif info.content.startswith('!!b drop'):
            args = info.content.strip().split(' ')[1:]
            if len(args) == 1:
                drop_items(info, 1, 10)
            elif len(args) == 3:
                start = int(args[1])
                end = int(args[2])
                drop_items(info, start, end)
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
    load_config(server)
    server.register_help_message('!!b', '一键批量召唤假人')
    server.register_event_listener('minecraft.console.info', on_user_info)
