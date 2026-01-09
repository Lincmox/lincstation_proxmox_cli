from lincmox_cli import __version__

import argparse
import textwrap

class CLI:

    __ASCII_TITLE = textwrap.dedent(f"""
██╗     ██╗███╗   ██╗ ██████╗███╗   ███╗ ██████╗ ██╗  ██╗
██║     ██║████╗  ██║██╔════╝████╗ ████║██╔═══██╗╚██╗██╔╝
██║     ██║██╔██╗ ██║██║     ██╔████╔██║██║   ██║ ╚███╔╝ 
██║     ██║██║╚██╗██║██║     ██║╚██╔╝██║██║   ██║ ██╔██╗ 
███████╗██║██║ ╚████║╚██████╗██║ ╚═╝ ██║╚██████╔╝██╔╝ ██╗
╚══════╝╚═╝╚═╝  ╚═══╝ ╚═════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝ v{__version__}
    """)

    def __init__(self, lincstation):
        self.lincstation = lincstation
        self._with_parser()._with_subparsers()._with_custom_help()

    def _cmd_status(self, args):
        print(self.lincstation)

    def _cmd_power(self, args):
        if args.action in ["on", "off"]:
            self.lincstation.set_power_led(args.action, args.color)
        elif args.action == "toggle":
            self.lincstation.toggle_power_led(args.choice)

    def _cmd_sata(self, args):
        if args.action in ["on", "off"]:
            self.lincstation.set_sata_led(args.num, args.action, args.color)
        elif args.action == "toggle":
            self.lincstation.toggle_sata_led(args.num, args.choice)

    def _cmd_nvme(self, args):
        if args.action in ["on", "off"]:
            self.lincstation.set_nvme_led(args.num, args.action, args.color)
        elif args.action == "toggle":
            self.lincstation.toggle_nvme_led(args.num, args.choice)

    def _cmd_network(self, args):
        if args.action in ["on", "off"]:
            self.lincstation.set_network_led(args.action, args.color)
        elif args.action == "toggle":
            self.lincstation.toggle_network_led(args.choice)

    def _cmd_strip_animation(self, args):
        self.lincstation.set_strip_animation(args.mode)

    def _cmd_strip_brightness(self, args):
        self.lincstation.set_strip_brightness(args.value)

    def _cmd_strip_color(self, args):
        self.lincstation.set_strip_color(args.r, args.g, args.b)

    def _cmd_strip_first_loop_color(self, args):
        self.lincstation.set_strip_first_loop_color(args.r, args.g, args.b)

    def _cmd_strip_second_loop_color(self, args):
        self.lincstation.set_strip_second_loop_color(args.r, args.g, args.b)

    def _cmd_reset(self, args):
        if args.mode == "full":
            self.lincstation.reset()
        elif args.mode == "leds":
            self.lincstation.reset_leds()
        elif args.mode == "strip":
            self.lincstation.reset_strip()

    def _with_parser(self):
        self.parser = argparse.ArgumentParser(
            description="LincMox - LincStation Proxmox CLI"
        )
        return self

    def _with_subparsers(self):
        self.sub = self.parser.add_subparsers(dest="command", required=True)
        return self

    def _with_custom_help(self):
        original_print_help = self.parser.print_help
        def print_help_with_title():
            print(self.__ASCII_TITLE)
            original_print_help()
        self.parser.print_help = print_help_with_title
        return self

    def with_status_cmd(self):
        p = self.sub.add_parser("status", help="Status")
        p.set_defaults(func=self._cmd_status)
        return self

    def with_power_cmd(self):
        p = self.sub.add_parser("power", help="Power LED control")
        power_sub = p.add_subparsers(dest="power_action", required=True)
        
        # Subcommands for 'on' and 'off' (require color)
        for action in ["on", "off"]:
            sp = power_sub.add_parser(action, help=f"Turn power LED {action}")
            sp.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
            sp.set_defaults(func=self._cmd_power, action=action)
        
        # Subcommand for 'toggle' (requires choice 1 or 2)
        sp = power_sub.add_parser("toggle", help="Toggle power LED")
        sp.add_argument("choice", choices=["on", "off"], help="Choice (on or off)")
        sp.set_defaults(func=self._cmd_power, action="toggle")
        
        return self

    def with_sata_cmd(self):
        p = self.sub.add_parser("sata", help="SATA LED control")
        p.add_argument("num", type=int, choices=[1, 2], help="SATA number")
        sata_sub = p.add_subparsers(dest="sata_action", required=True)
        
        # Subcommands for 'on' and 'off' (require color)
        for action in ["on", "off"]:
            sp = sata_sub.add_parser(action, help=f"Turn SATA LED {action}")
            sp.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
            sp.set_defaults(func=self._cmd_sata, action=action)
        
        # Subcommand for 'toggle' (requires choice on or off)
        sp = sata_sub.add_parser("toggle", help="Toggle SATA LED")
        sp.add_argument("choice", choices=["on", "off"], help="Choice (on or off)")
        sp.set_defaults(func=self._cmd_sata, action="toggle")
        
        return self

    def with_nvme_cmd(self):
        p = self.sub.add_parser("nvme", help="NVMe LED control")
        p.add_argument("num", type=int, choices=[1,2,3,4], help="NVMe number")
        nvme_sub = p.add_subparsers(dest="nvme_action", required=True)
        
        # Subcommands for 'on' and 'off' (require color)
        for action in ["on", "off"]:
            sp = nvme_sub.add_parser(action, help=f"Turn NVMe LED {action}")
            sp.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
            sp.set_defaults(func=self._cmd_nvme, action=action)
        
        # Subcommand for 'toggle' (requires choice on or off)
        sp = nvme_sub.add_parser("toggle", help="Toggle NVMe LED")
        sp.add_argument("choice", choices=["on", "off"], help="Choice (on or off)")
        sp.set_defaults(func=self._cmd_nvme, action="toggle")
        
        return self

    def with_network_cmd(self):
        p = self.sub.add_parser("network", help="Network LED control")
        network_sub = p.add_subparsers(dest="network_action", required=True)
        
        # Subcommands for 'on' and 'off' (require color)
        for action in ["on", "off"]:
            sp = network_sub.add_parser(action, help=f"Turn Network LED {action}")
            sp.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
            sp.set_defaults(func=self._cmd_network, action=action)
        
        # Subcommand for 'toggle' (requires choice on or off)
        sp = network_sub.add_parser("toggle", help="Toggle Network LED")
        sp.add_argument("choice", choices=["on", "off"], help="Choice (on or off)")
        sp.set_defaults(func=self._cmd_network, action="toggle")
        
        return self

    def _with_strip_animation_cmd(self):
        p = self.sub.add_parser("strip_animation", help="Set LED strip animation")
        p.add_argument("mode", choices=["off", "breath", "loop"], help="Animation mode")
        p.set_defaults(func=self._cmd_strip_animation)
        return self

    def _with_strip_brightness_cmd(self):
        p = self.sub.add_parser("strip_brightness", help="Set LED strip brightness")
        p.add_argument("value", type=int, choices=range(0, 256), help="Brightness value (0-255)")
        p.set_defaults(func=self._cmd_strip_brightness)
        return self

    def _with_strip_color_cmd(self):
        p = self.sub.add_parser("strip_color", help="Set LED strip color")
        p.add_argument("r", type=int, choices=range(0, 256), help="Red value (0-255)")
        p.add_argument("g", type=int, choices=range(0, 256), help="Green value (0-255)")
        p.add_argument("b", type=int, choices=range(0, 256), help="Blue value (0-255)")
        p.set_defaults(func=self._cmd_strip_color)
        return self

    def _with_strip_first_loop_color_cmd(self):
        p = self.sub.add_parser("strip_first_loop_color", help="Set LED strip first loop color")
        p.add_argument("r", type=int, choices=range(0, 256), help="Red value (0-255)")
        p.add_argument("g", type=int, choices=range(0, 256), help="Green value (0-255)")
        p.add_argument("b", type=int, choices=range(0, 256), help="Blue value (0-255)")
        p.set_defaults(func=self._cmd_strip_first_loop_color)
        return self

    def _with_strip_second_loop_color_cmd(self):
        p = self.sub.add_parser("strip_second_loop_color", help="Set LED strip second loop color")
        p.add_argument("r", type=int, choices=range(0, 256), help="Red value (0-255)")
        p.add_argument("g", type=int, choices=range(0, 256), help="Green value (0-255)")
        p.add_argument("b", type=int, choices=range(0, 256), help="Blue value (0-255)")
        p.set_defaults(func=self._cmd_strip_second_loop_color)
        return self

    def with_strip_cmds(self):
        return (self
                ._with_strip_animation_cmd()
                ._with_strip_brightness_cmd()
                ._with_strip_color_cmd()
                ._with_strip_first_loop_color_cmd()
                ._with_strip_second_loop_color_cmd())

    def with_reset_cmd(self):
        p = self.sub.add_parser("reset", help="Reset all LEDs and strip")
        p.add_argument("mode", choices=["full", "leds", "strip"], help="Reset mode")
        p.set_defaults(func=self._cmd_reset)
        return self

    def build(self):
        args = self.parser.parse_args()
        args.func(args)
