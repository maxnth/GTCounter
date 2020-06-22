import csv
from typing import Dict
from pathlib import Path
import xml.etree.ElementTree as ET


def get_namespace(root: ET.Element) -> Dict[str, str]:
    return {"page": root.tag.split('}')[0].strip('{')}


def export_stats(stats: dict, output_dir: Path):
    csv_header = ["Project", "Lines of ground truth"]
    try:
        with Path(output_dir, "stats.csv").open("w") as statsfile:
            writer = csv.DictWriter(statsfile, fieldnames=csv_header)
            writer.writeheader()
            for dir in stats:
                writer.writerow({'Project': dir, 'Lines of ground truth': stats[dir]})
    except IOError as e:
        raise e


def cprint(fmt, fg=None, bg=None, style=None):
    """
    Colour-printer.

        cprint( 'Hello!' )                                  # normal
        cprint( 'Hello!', fg='g' )                          # green
        cprint( 'Hello!', fg='r', bg='w', style='bx' )      # bold red blinking on white

    List of colours (for fg and bg):
        k   black
        r   red
        g   green
        y   yellow
        b   blue
        m   magenta
        c   cyan
        w   white

    List of styles:
        b   bold
        i   italic
        u   underline
        s   strikethrough
        x   blinking
        r   reverse
        y   fast blinking
        f   faint
        h   hide
    """

    COLCODE = {
        'k': 0, # black
        'r': 1, # red
        'g': 2, # green
        'y': 3, # yellow
        'b': 4, # blue
        'm': 5, # magenta
        'c': 6, # cyan
        'w': 7  # white
    }

    FMTCODE = {
        'b': 1, # bold
        'f': 2, # faint
        'i': 3, # italic
        'u': 4, # underline
        'x': 5, # blinking
        'y': 6, # fast blinking
        'r': 7, # reverse
        'h': 8, # hide
        's': 9, # strikethrough
    }

    # properties
    props = []
    if isinstance(style, str):
        props = [FMTCODE[s] for s in style]
    if isinstance(fg, str):
        props.append(30 + COLCODE[fg])
    if isinstance(bg, str):
        props.append(40 + COLCODE[bg])

    # display
    props = ';'.join([str(x) for x in props])
    if props:
        print('\x1b[%sm%s\x1b[0m' % (props, fmt))
    else:
        print(fmt)
