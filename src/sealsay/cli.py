import argparse
import logging
import math
import os
import platform
import secrets
import sys
import textwrap
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from importlib.resources import files
from importlib.resources.abc import Traversable
from pathlib import Path

# the magic numbers in sys.exit were pmo AND os.EX_* stuff isn't cross-platform, so stupid
EXIT_NOT_FOUND = 3
EXIT_INVALID_SEAL = 4
EXIT_IO_ERROR = 5
EXIT_INTERRUPTED = 130  # (128 + SIGINT is how unix does it)

# https://github.com/Code-Hex/Neo-cowsay/blob/f68c20f068c26c55bc5a8572f1c582f0a1b08d34/decoration/rainbow.go
# Thank you, Neo-cosway (the aurora and rainbow logic is entirely stolen)
#
RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN = 31, 32, 33, 34, 35, 36
RAINBOW_COLORS = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]
RAINBOW_FREQ = 0.1

type SealSource = Traversable | Path


def _user_seals_dir() -> Path | None:
    match platform.system():
        case "Windows":
            if appdata := os.environ.get("APPDATA"):
                candidate = Path(appdata) / "sealsay" / "seals"
                if candidate.is_dir():
                    return candidate
        case "Darwin":  # mac os
            candidate = Path.home() / "Library" / "Application Support" / "sealsay" / "seals"
            if candidate.is_dir():
                return candidate
        case _:  # linux/unix
            if xdg_data_home := os.environ.get("XDG_DATA_HOME"):
                candidate = Path(xdg_data_home) / "sealsay" / "seals"
            else:
                candidate = Path.home() / ".local" / "share" / "sealsay" / "seals"
            if candidate.is_dir():
                return candidate

    return None


def _package_seals_dir() -> Traversable:
    return files("sealsay").joinpath("seals")


def _seal_sources() -> dict[str, SealSource]:
    sources = {
        entry.name: entry
        for entry in _package_seals_dir().iterdir()
        if entry.is_file() and entry.name.endswith(".txt")
    }

    if user_dir := _user_seals_dir():
        for entry in sorted(user_dir.glob("*.txt")):
            sources[entry.name] = entry

    return sources


def _read_seal_text(source: SealSource) -> str:
    return source.read_text(encoding="utf-8")


SEAL_SOURCES = _seal_sources()
log = logging.getLogger("sealsay")


def emit(line: str = "") -> None:
    sys.stdout.write(line + "\n")


def _positive_int(s: str) -> int:
    try:
        v = int(s)
    except ValueError as e:
        msg = f"must be a positive integer, got {s!r}"
        raise argparse.ArgumentTypeError(msg) from e
    if v < 1:
        msg = f"must be >=1, got {v}"
        raise argparse.ArgumentTypeError(msg)
    return v


def _make_parser_skeleton() -> tuple[
    argparse.ArgumentParser,
    argparse._MutuallyExclusiveGroup,  # pyright: ignore[reportPrivateUsage]
    argparse.Action,
]:
    p = argparse.ArgumentParser(
        prog="sealsay",
        description="CLI app that generates ASCII art of a seal saying a message",
        formatter_class=argparse.RawDescriptionHelpFormatter,  # turns off text wrapping in epilog
        epilog=(
            "e.g usage:\n"
            f"{'':<{3}}sealsay -s 'Hello, world!' # uses the 'basic' seal\n"
            f"{'':<{3}}sealsay -r Hi              # chooses a random seal"
        ),
    )
    p.add_argument("message", nargs="*", help="text for the seal to say")
    p.add_argument("-l", "--list", action="store_true", help="lists all seals")
    p.add_argument(
        "-r", "--random", action="store_true", help="pick a random seal to display your message"
    )
    p.add_argument("-n", "--no-wrap", action="store_true", help="disable text wrapping")
    p.add_argument(
        "-w",
        "--wrap",
        type=_positive_int,
        default=40,
        metavar="int",
        help="wrap column after a given amount of chars (default = 40)",
    )
    p.add_argument(
        "-e",
        "--eyes",
        default=None,
        metavar="EE",
        help="gives your seal eyes!! comma separated for seals with multiple eyes. e.g 'aa,bb,cc'",
    )
    p.add_argument(
        "-T",
        "--tongues",
        default=None,
        metavar="TT",
        help="gives your seal a tongue!! comma separated for seals with multiple "
        "tongues. e.g 'aa,bb,cc'",
    )

    appearance = p.add_argument_group("appearance")
    appearance.add_argument("-B", "--bold", action="store_true", help="makes bubble text bolded")
    appearance.add_argument(
        "-R", "--rainbow", action="store_true", help="makes bubble text rainbow"
    )
    appearance.add_argument(
        "-A", "--aurora", action="store_true", help="makes bubble text aurora'd"
    )

    seal_group = p.add_argument_group("seals")
    seal_choice = seal_group.add_mutually_exclusive_group(required=False)
    say_action = seal_choice.add_argument(
        "-s",
        "--say",
        dest="seal",
        action="store_const",
        const=None,
        help="says something with the og seal",
    )

    return p, seal_choice, say_action


_SHORT_FLAG_LEN = 2


def _reserved_flags() -> tuple[frozenset[str], frozenset[str]]:
    skeleton, _, _ = _make_parser_skeleton()
    short: set[str] = set()
    long_: set[str] = set()
    for opt in skeleton._option_string_actions:  # noqa: SLF001
        if opt.startswith("--"):
            long_.add(opt[2:])
        elif len(opt) == _SHORT_FLAG_LEN:
            short.add(opt[1])
    return frozenset(short), frozenset(long_)


_RESERVED_SHORT, _RESERVED_LONG = _reserved_flags()


# finds all .txt's in filePath (seals dir), stems them to first char
# and makes a list of callable flags from the stems.
#
# New seals now won't require code changes, just a new .txt
#
# Flag collisions are handled by extending prefix by one char until a unique flag is found
# we also check if the flag is reserved by our cli's actual flags
def _build_seal_map(sources: Mapping[str, SealSource]) -> dict[str, str]:
    seals: dict[str, str] = {}
    used_short = set(_RESERVED_SHORT)
    for filename in sorted(sources, key=lambda name: Path(name).stem):
        stem = Path(filename).stem
        n = 1
        while n <= len(stem) and stem[:n] in used_short:
            n += 1
        if n > len(stem):
            seals[f"--{stem}"] = filename
        else:
            prefix = stem[:n]
            used_short.add(prefix)
            seals[f"-{prefix}"] = filename
    return seals


SEALS = _build_seal_map(SEAL_SOURCES)


def _add_seal_flags(
    seal_choice: argparse._MutuallyExclusiveGroup,  # pyright: ignore[reportPrivateUsage]
    say_action: argparse.Action,
) -> None:
    for flag in sorted(SEALS):
        name = Path(SEALS[flag]).stem
        long_flag = f"--{name}"
        # skip if long name == short name or if it is reserved by cli
        flags = [flag] if flag == long_flag or name in _RESERVED_LONG else [flag, long_flag]
        seal_choice.add_argument(
            *flags, dest="seal", action="store_const", const=flag, help=f"{name} seal"
        )

    basic_flag = next((f for f, n in SEALS.items() if Path(n).stem == "basic"), None)
    if basic_flag:
        say_action.const = basic_flag


def build_parser() -> argparse.ArgumentParser:
    p, seal_choice, say_action = _make_parser_skeleton()
    _add_seal_flags(seal_choice, say_action)
    return p


# helper to dedupe the colorizers
def _colorize(
    text: str, color_for: Callable[[int], str], *, bold: bool = False, reset_on_nl: bool = False
) -> str:
    attr = ";1" if bold else ""
    buf: list[str] = []
    i = 0

    for ch in text:
        if ch == "\n":
            if reset_on_nl:
                i = 0

            buf.append(ch)
            continue

        buf.append(f"\x1b[{color_for(i)}{attr}m{ch}\x1b[0m")
        i += 1

    return "".join(buf)


# this is such a shit function but idc
def _aurora_index(i: int) -> int:
    r = int(6 * ((math.sin(RAINBOW_FREQ * i + 0) * 127 + 128) / 256)) * 36
    g = int(6 * ((math.sin(RAINBOW_FREQ * i + 2 * (math.pi / 3)) * 127 + 128) / 256)) * 6
    b = int(6 * ((math.sin(RAINBOW_FREQ * i + 4 * (math.pi / 3)) * 127 + 128) / 256)) * 1

    return 16 + r + g + b


def rainbow_print(text: str, *, bold: bool = False) -> str:
    return _colorize(
        text, color_for=lambda i: str(RAINBOW_COLORS[i % 6]), bold=bold, reset_on_nl=True
    )


def aurora_print(text: str, *, bold: bool = False) -> str:
    return _colorize(text, color_for=lambda i: f"38;5;{_aurora_index(i)}", bold=bold)


# strips '# eye: value' and returns (seal_art, defaults)
def _parse_seal(raw: str) -> tuple[str, dict[str, str]]:
    defaults: dict[str, str] = {}
    lines = raw.splitlines(keepends=True)
    body_start = 0

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith("#") and ":" in stripped:
            key, _, val = stripped[1:].partition(":")
            defaults[key.strip()] = val.strip()
            body_start = i + 1
        else:
            break

    return "".join(lines[body_start:]), defaults


def _parse_braced(mark: str) -> tuple[str, list[tuple[int, int]]]:
    parts: list[str] = []
    regions: list[tuple[int, int]] = []
    pos = 0
    i = 0

    while i < len(mark):
        if mark[i] == "{":
            close = mark.find("}", i + 1)
            if close < 0:
                parts.append(mark[i])
                pos += 1
                i += 1
                continue
            region = mark[i + 1 : close]
            parts.append(region)
            regions.append((pos, len(region)))
            pos += len(region)
            i = close + 1
        else:
            parts.append(mark[i])
            pos += 1
            i += 1

    return "".join(parts), regions


def _fill_regions(literal: str, regions: list[tuple[int, int]], user_input: str) -> str:
    out: list[str] = []
    last = 0
    idx = 0

    for start, width in regions:
        out.append(literal[last:start])
        out.append(user_input[idx : idx + width].ljust(width))
        idx += width
        last = start + width

    out.append(literal[last:])
    return "".join(out)


# applies user provided eyes/tongues
def _apply_substitution(art: str, marks: list[str], user_input: str | None) -> str:
    if user_input is None or not marks:
        return art

    values = [v.strip() for v in user_input.split(",")]
    if len(values) == 1:
        values = values * len(marks)

    for original, new in zip(marks, values, strict=False):
        literal, regions = _parse_braced(original)
        art = art.replace(literal, _fill_regions(literal, regions, new), 1)
    return art


@dataclass(frozen=True)
class RenderStyle:
    no_wrap: bool = False
    wrap: int = 40
    bold: bool = False
    rainbow: bool = False
    aurora: bool = False


def print_seal(message: str, seal_art: str, style: RenderStyle) -> None:
    message = message or ""

    lines: list[str] = []
    for paragraph in message.split("\n"):
        if style.no_wrap:
            lines.append(paragraph)
        else:
            lines.extend(textwrap.wrap(paragraph, width=style.wrap) or [""])

    width = max(len(line) for line in lines)

    # helper func for border deduplication
    def border(char: str) -> str:
        leader = " "
        inner_width = width + 2

        return leader + char * inner_width

    top = border("_")
    bottom = border("-")

    if len(lines) == 1:
        body = f"< {lines[0].ljust(width)} >"
    else:
        body_lines: list[str] = []

        last = len(lines) - 1
        sides = {0: ("/", "\\"), last: ("\\", "/")}

        for i, line in enumerate(lines):
            left, right = sides.get(i, ("|", "|"))
            body_lines.append(f"{left} {line.ljust(width)} {right}")
        body = "\n".join(body_lines)

    output = f"{top}\n{body}\n{bottom}\n{seal_art}"

    if style.rainbow:
        output = rainbow_print(output, bold=style.bold)
    elif style.aurora:
        output = aurora_print(output, bold=style.bold)
    elif style.bold:
        output = f"\x1b[1m{output}\x1b[0m"

    emit(output)


def select_seal(seal_var: str | None, eyes: str | None, tongues: str | None) -> str | None:
    if seal_var not in SEALS:
        return None

    source = SEAL_SOURCES[SEALS[seal_var]]

    try:
        raw = _read_seal_text(source)
    except FileNotFoundError:
        log.exception("Error: seal file not found: %s", source)
        sys.exit(EXIT_INVALID_SEAL)

    art, default = _parse_seal(raw)
    eye_pairs = [p.strip() for p in default.get("eyes", "").split(",") if p.strip()]
    tongue_marks = [t.strip() for t in default.get("tongues", "").split(",") if t.strip()]

    art = _apply_substitution(art, eye_pairs, eyes)
    return _apply_substitution(art, tongue_marks, tongues)


def read_stdin() -> str:
    try:
        return sys.stdin.read().rstrip("\n")
    except KeyboardInterrupt:
        sys.exit(EXIT_INTERRUPTED)
    except (OSError, UnicodeDecodeError):
        log.exception("Error when reading from stdin")
        sys.exit(EXIT_IO_ERROR)


def list_seals() -> None:
    if not SEALS:
        log.error("No seals found")
        sys.exit(EXIT_NOT_FOUND)

    emit("Available seals:")
    for flag in sorted(SEALS):
        emit(f"{'':<{3}}{flag} {Path(SEALS[flag]).stem}")


def main() -> None:
    logging.basicConfig(level=logging.WARNING, format="%(message)s", stream=sys.stderr)
    parser = build_parser()
    args = parser.parse_args()

    if args.list:
        list_seals()
        return

    if args.random:
        if not SEALS:
            log.error("No seals found")
            sys.exit(EXIT_NOT_FOUND)
        args.seal = secrets.choice(list(SEALS.keys()))

    message = " ".join(args.message)
    if not message and not sys.stdin.isatty():
        message = read_stdin()

    if (seal_art := select_seal(args.seal, eyes=args.eyes, tongues=args.tongues)) is None:
        parser.error(f'please provide something so we can make seal instead of "{args.seal}"')

    use_color = sys.stdout.isatty() and not os.environ.get("NO_COLOR")
    style = RenderStyle(
        no_wrap=args.no_wrap,
        wrap=args.wrap,
        bold=args.bold and use_color,
        rainbow=args.rainbow and use_color,
        aurora=args.aurora and use_color,
    )
    print_seal(message, seal_art, style)
