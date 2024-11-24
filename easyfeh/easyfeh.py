"""
███████╗ █████╗ ███████╗██╗   ██╗███████╗███████╗██╗  ██╗
██╔════╝██╔══██╗██╔════╝╚██╗ ██╔╝██╔════╝██╔════╝██║  ██║
█████╗  ███████║███████╗ ╚████╔╝ █████╗  █████╗  ███████║
██╔══╝  ██╔══██║╚════██║  ╚██╔╝  ██╔══╝  ██╔══╝  ██╔══██║
███████╗██║  ██║███████║   ██║   ██║     ███████╗██║  ██║
╚══════╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝     ╚══════╝╚═╝  ╚═╝ 
By Shibam Roy
"""

## Modules ##=========================================================================================
# import traceback # Occasionally for debugging
from sys import stdout
from .conf import *
from .functions import *
from argparse import ArgumentParser
from sys import stdout
from rich.panel import Panel

class ArgP(ArgumentParser):
    def _print_help(self,file=None):
        c.print(helpTxt)
        lines=[]
        for action in self._actions:
            opts=action.option_strings
            cmd_lines=[]
            hlp=action.help
            if hlp=="":

                ## Exceptions to be handled manually
                if "-ui" in opts:
                    s="[bold]easyfeh -r -ui[/bold]       -> [green]Sets a random wallpaper from the internet[/green]\nor [bold]easyfeh --random --use-internet[/bold]"
                    lines.append(s)
                elif "-ud" in opts:
                    s="[bold]easyfeh -r -ud[/bold]       -> [green]Sets a random wallpaper which is already downloaded from the internet[/green]\nor [bold]easyfeh --random --use-internet[/bold]"
                    lines.append(s)
                elif "-q" in opts:
                    s="[bold]easyfeh -d [blue]<amount>[/blue] -q [blue]<query>[/blue] -s [blue]<source>[/blue][/bold]       -> [green]Download wallpapers [white](Doesn't set them)\nor [bold]easyfeh --query [blue]<query>[/blue] --source [blue]<source>[/blue][/bold]\n\n(Optional arguments: -q, -s ; If not specified, it will check configuration)(Source options: wallhaven(default), unsplash)[/white][/green]"
                    lines.append(s)

            else:
                if opts==[]:
                    cmd_lines.append("easyfeh [blue]<some_image_path>[/blue]")
                for i in opts:
                    cmd_lines.append(f"easyfeh {i}")
                s=f"[bold]{cmd_lines[0]}[/bold]     -> [green]{hlp}[/green]"
                for ind,cmd in enumerate(cmd_lines):
                    if ind!=0:
                        s+=f"\nor [bold]{cmd}[/bold]"
                lines.append(s)
        
        options = "\n\n".join(lines)

        c.print(Panel(options, border_style="blue"))
        c.print("\n[red]The configuration file for easyfeh can be found at $HOME/.config/easyfeh/config.toml[/red]")

    def print_help(self,file=None):
        if file is None:
            file=stdout
        self._print_help(file)

    def error(self,message):
        if "unrecognized" in message:
            c.print("[red]No such command found:( [/red] , try running [green]'easyfeh -h'[/green]")
            self.exit(2)
        else:
            c.print(f"[bold red]Error: {message}[/bold red]")
            self.exit(2)
        

def main():
## Loading Configuration ##========================================================================
    with open(config_path, "r") as f:
        config = load(f)

## Main Program ##======================================================================
    parser=ArgP(add_help=False)
    parser.add_argument("-h","--help",action="store_true",help="Prints this help message")

    parser.add_argument("img",nargs="?",type=str,help="Sets the wallpaper which was last used [white](Sets random if no history is saved, needs random to be enabled in that case)[/white]")

    parser.add_argument("-res","--restore",action="store_true",help="Sets the wallpaper which was last used [white](Sets random if no history is saved, needs random to be enabled in that case)[/white]")

    parser.add_argument("-p","--prev",action="store_true",help="Sets previous wallpaper [white](Requires wallpaper history to be turned on)[/white]")
    
    parser.add_argument("-n","--next",action="store_true",help="Sets next wallpaper [white](requires wallpaper history to be turned on)[/white]")

    parser.add_argument("-r","--random",action="store_true",help="Sets a random wallpaper (directory for random wallpaper must be configured or internet wallpapers should be turned on)")

    parser.add_argument("-ui","--use-internet",action="store_true",help="")
    parser.add_argument("-ud","--use-down",action="store_true",help="")

    parser.add_argument("-rh","--reset-hist",action="store_true",help="[bold underline red]WARNING[/bold underline red] Resets the wallpaper history [white] (Keeps the last used wallpaper,Take backups before running this!)[/white]")

    parser.add_argument("-rw","--reset-walls",action="store_true",help="[bold underline red]WARNING[/bold underline red] Deletes the wallpapers downloaded from internet[white] (Take backups before running this!)[/white]")
    
    parser.add_argument("-rc","--reset-conf",action="store_true",help="[bold underline red]WARNING[/bold underline red] Deletes existing configuration and resets to default[white] (Take backups before running this!)[/white]")

    parser.add_argument("-dl","--delete-last",action="store_true",help="[bold underline red]WARNING[/bold underline red] Deletes last used wallpaper[white] (Wallpaper before current, Take backups before running this!)[/white]")

    parser.add_argument("-sh","--show-hist",action="store_true",help="Prints out history")

    parser.add_argument("-sd","--show-down",action="store_true",help="Prints out all the wallpapers downloaded from internet [white](If any)[/white]")

    parser.add_argument("-sc","--show-curr",action="store_true",help="Prints out the path to the current wallpaper [white](last used, requires wallpaper history to be turned on)[/white]")

    parser.add_argument("-d","--download",type=int,help="Download wallpapers[white](Doesn't set them)[/white]")
    parser.add_argument("-q","--query",type=str,help="")
    parser.add_argument("-s","--source",choices=['unsplash', 'wallhaven'],help="")

    args=parser.parse_args()

    if args.help:
        parser.print_help()
    if args.img:
        setWall(args.img)
        
    if args.restore:
        try:
            with open(path.join(config_directory, "history.txt"), "r") as f:
                walls = f.readlines()
                p=walls[config["internal"]["wall_index"]].replace("\n","")
                if not path.isfile(p):
                    raise FileNotFoundError
                else:
                    setWall(p, save=False)
                    print("Set to last used wallpaper!")
        except:
            c.print("[red]File not found[/red], ",end="")
            if getConf("internet","use_from_internet"):
                print("fetching from internet")
                setRandom(config,use_internet=True)
            else:
                print("setting a random one")
                setRandom(config)

    if args.reset_hist:
        confirm=c.input("[yellow]Are you sure you want to clear your history? (y/n) :[/yellow]")
        if confirm.lower()=="y":
            resetHistory(getConf("internal", "wall_index"))
            print("Done!")
        else:
            print("Aborted...")
    if args.reset_conf:
        confirm=c.input("[yellow]Are you sure you want to reset your configuration? (y/n) :[/yellow]")
        if confirm.lower()=="y":
            write_defaults()
            print("Done!")
        else:
            print("Aborted...")
    if args.reset_walls:
        confirm=c.input("[yellow]Are you sure you want to delete all wallpapers ? (y/n) :[/yellow]")
        if confirm.lower()=="y":
            resetDownloaded()
            print("Done!")
        else:
            print("Aborted...")
    if args.delete_last:
            confirm=c.input("[yellow]Are you sure you want to delete the last used wallpaper(wallpaper before current)? (y/n) :[/yellow]")
            if confirm.lower()=="y":
                deleteLast()
            else:
                print("Aborted...")
    if args.prev:
        try:
            with open(history_path, "r") as f:
                walls = f.readlines()
                newIndex = int(config["internal"]["wall_index"]) - 1
                toSet = walls[newIndex].replace("\n","")
                if path.isfile(toSet):
                    setWall(toSet, save=False)
                    config["internal"]["wall_index"] = newIndex
                    setConf(config)
                else:
                    c.print("[red]Previous wallpaper doesn't exist anymore...[/red]")
        except:
            c.print(
                    "[red]Error: No previous wallpaper found. [/red](Maybe already on oldest, Check history!)"
            )
    if args.next:
        try:
            with open(history_path, "r") as f:
                walls = f.readlines()
                newIndex = int(config["internal"]["wall_index"]) + 1
                if newIndex != 0:
                    config["internal"]["wall_index"] = newIndex
                    setConf(config)
                    toSet = walls[newIndex].replace("\n","")
                    if path.isfile(toSet):
                        setWall(toSet, save=False)
                    else:
                        c.print("[red]Next wallpaper doesn't exist anymore...[/red]")
                else:
                    c.print(
                            "[red]Error: No next wallpaper found. [/red](Maybe already on latest, Check history!)"
                    )
        except:
            c.print(
                    "[red]Error: No next wallpaper found. [/red](Maybe already on latest, Check history!)"
            )
    if args.random and args.use_internet:
        setRandom(config, use_internet=True)
    elif args.random and args.use_down:
        setRandom(config,use_down=True)
    elif args.random:
        if getConf("internet","use_from_internet"):
            setRandom(config,use_internet=True)
        else:
            setRandom(config)
    if args.show_hist:
        printHistory()

    if args.show_down:
        listInstalled()
    if args.show_curr:
        showCurrent()
    if args.download:
        amount=args.download
        source="wallhaven"
        query=getConf("internet","image_query")

        if args.source:
            source=args.source
        if args.query:
            query=args.query

        c.print(f"Searching for [green]{query}[/green] in [green]{source}[/green]")
        d=Downloader(query,source=returnSourceParam(source))
        d.download(count=amount)
        c.print(f"[green]Successfully downloaded [yellow]{amount}[/yellow] wallpaper(s)![/green]")
    if not any(vars(args).values()): 
        c.print("[red]No arguments provided...[/red] , try running [green]'easyfeh -h'[/green]")
            
if __name__=="__main__":
    main()
