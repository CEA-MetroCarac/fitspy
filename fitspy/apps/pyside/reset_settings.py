import argparse
from PySide6.QtCore import QSettings


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="fitspy", description="Fitspy command-line utilities")
    sub = p.add_subparsers(dest="command", required=True)

    rs = sub.add_parser("reset-settings", help="Clear stored GUI settings (QSettings)")
    rs.add_argument("--org", default="CEA-MetroCarac", help="QSettings organization name")
    rs.add_argument("--app", default="Fitspy", help="QSettings application name")
    rs.add_argument("--list", action="store_true", help="List current keys and exit")
    rs.add_argument(
        "--yes", "-y",
        action="store_true",
        help="Do not prompt for confirmation (recommended for scripts)",
    )

    return p


def reset_settings(org: str = "CEA-MetroCarac", app: str = "Fitspy", *, assume_yes: bool = False) -> int:
    settings = QSettings(org, app)

    keys = list(settings.allKeys())
    if not keys:
        print(f"No settings found for org={org!r} app={app!r}.")
        return 0

    if not assume_yes:
        print(f"About to delete {len(keys)} setting(s) for org={org!r} app={app!r}.")
        resp = input("Proceed? [y/N] ").strip().lower()
        if resp not in ("y", "yes"):
            print("Aborted.")
            return 2

    settings.clear()
    settings.sync()
    print(f"Deleted {len(keys)} setting(s) for org={org!r} app={app!r}.")
    return 0

def list_settings(org: str = "CEA-MetroCarac", app: str = "Fitspy") -> None:
    settings = QSettings(org, app)
    keys = list(settings.allKeys())
    if not keys:
        print(f"No settings found for org={org!r} app={app!r}.")
        return

    for k in keys:
        value = settings.value(k)
        print(f"{k} = {value!r}")


def main(argv: list[str] | None = None) -> int:
    parser = _build_parser()
    args = parser.parse_args(argv)

    if args.command == "reset-settings":
        if args.list:
            list_settings(args.org, args.app)
            return 0
        return reset_settings(args.org, args.app, assume_yes=args.yes)

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())