from asyncio import sleep as _sleep
from ctypes import windll
from json import dump, load
from os import system

from discord import Intents
from discord.ext.commands import Bot
from pypresence import Presence
from rich import print
from rich.console import Console

console = Console()
cdp = Bot(
    command_prefix="+@[1!", # Not a self-bot, don't even try run command's because they wont work.
    self_bot=True,
    fetch_offline_members=False,
    intents=Intents.all()
    )
cdp.remove_command('help')

def fetch_json(filename: str, Option):
    f = open(filename)
    data = load(f)
    f.close()
    return str(data[Option])


def write_json():
    system('cls')
    token = console.input("[bold cyan][INPUT][/bold cyan] [bold white]Please enter Discord Token: [/bold white]")
    rpid = console.input("[bold cyan][INPUT][/bold cyan] [bold white]Please enter Discord Application ID[/bold white] [bold cyan](Rich Presence)[/bold cyan][bold white]: [/bold white]")
    config = {"token": token, "rpid": rpid, "developer": "bucky#9990"}
    
    with open('config.json', 'w') as f:
        dump(config, f)


def status_write():
    rpcState = console.input("[bold cyan][INPUT][/bold cyan] [bold white]Please enter what you would like State to become: [/bold white]")
    rpcDetails = console.input("[bold cyan][INPUT][/bold cyan] [bold white]Please enter what you would like State Details to become: [/bold white]")
    rpcL_Image_Name = console.input("[bold cyan][INPUT][/bold cyan] [bold white]Please enter Large Image Asset name: [/bold white]")
    rpcS_Image_Name = console.input("[bold cyan][INPUT][/bold cyan] [bold white]Please enter Small Image Asset name: [/bold white]")
    status = {"rpcState": rpcState, "rpcDetails": rpcDetails, "rpcS_Image_Name": rpcS_Image_Name, "rpcL_Image_Name": rpcL_Image_Name, "developer": "bucky#9990"}
    
    with open('status.json', 'w') as f:
        dump(status, f)


try:
    fetch_json("config.json", "developer")
except:
    rpid = fetch_json("config.json", "rpid")
    print(f"[bold cyan][INFO][/bold cyan] [bold white] To add Image assets please head over to https://discord.com/developers/applications/{rpid}/rich-presence/assets[/bold white]")
    write_json()

try:
    fetch_json("status.json", "developer")
except:
    status_write()
RPC = Presence(fetch_json("config.json", "rpid"))
RPC.connect()

@cdp.event
async def on_ready():
    system('cls')
    renew_check = console.input("[bold yellow][IMPORTANT][/bold yellow] [bold white]Do you want to Change your Previous Status or not? (y/n) [/bold white]")
    if renew_check.lower() == "n":
        try:
            RPC.update(
                state=fetch_json("status.json", "rpcState"),
                details=fetch_json("status.json", "rpcDetails"),
                large_image=fetch_json("status.json", "rpcL_Image_Name"),
                small_image=fetch_json("status.json", "rpcS_Image_Name")
                )
        except Exception as e:
            random = e
            windll.kernel32.SetConsoleTitleW(f"Discord Custom Presence | Developer - bucky#9990")
            console.print("[bold cyan][INFO][/bold cyan] [bold green]Your Custom Presence is ready.[/bold green]")
    elif renew_check.lower() == "y":
        status_write()
        print("[red][IMPORTANT] Please rerun the file.[/red]")
        await _sleep(2)
        exit()

cdp.run(fetch_json("config.json", "token"), bot=False)