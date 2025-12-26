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
        self.lincstation.set_power_led(args.action, args.color)

    def _cmd_sata(self, args):
        self.lincstation.set_sata_led(args.num, args.action, args.color)

    def _cmd_nvme(self, args):
        self.lincstation.set_nvme_led(args.num, args.action, args.color)

    def _cmd_network(self, args):
        self.lincstation.set_network_led(args.action, args.color)

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
        p.add_argument("action", choices=["on", "off"], help="Action")
        p.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
        p.set_defaults(func=self._cmd_power)
        return self

    def with_sata_cmd(self):
        p = self.sub.add_parser("sata", help="SATA LED control")
        p.add_argument("num", type=int, choices=[1, 2], help="SATA number")
        p.add_argument("action", choices=["on", "off"], help="Action")
        p.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
        p.set_defaults(func=self._cmd_sata)
        return self

    def with_nvme_cmd(self):
        p = self.sub.add_parser("nvme", help="NVMe LED control")
        p.add_argument("num", type=int, choices=[1,2,3,4], help="NVMe number")
        p.add_argument("action", choices=["on", "off"], help="Action")
        p.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
        p.set_defaults(func=self._cmd_nvme)
        return self

    def with_network_cmd(self):
        p = self.sub.add_parser("network", help="Network LED control")
        p.add_argument("action", choices=["on", "off"], help="Action")
        p.add_argument("color", choices=["white", "red", "orange"], help="Color to set")
        p.set_defaults(func=self._cmd_network)
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

    def build(self):
        args = self.parser.parse_args()
        args.func(args)
