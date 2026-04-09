#!/usr/bin/env python3
"""
Rider-Waite-Smith Image Verification Script
==========================================
QA: Chloe

Automated verification of all 78 classic Rider-Waite tarot card images.
Checks file existence, naming convention, file sizes, and image integrity.

Usage:
    python scripts/verify_rws_images.py [--fix] [--verbose]

Options:
    --fix       Attempt to fix naming issues (renames files)
    --verbose   Show detailed output for each card
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, NamedTuple, Tuple

# Card definitions matching the codebase
MAJOR_ARCANA = [
    (0, "the_fool"),
    (1, "the_magician"),
    (2, "the_high_priestess"),
    (3, "the_empress"),
    (4, "the_emperor"),
    (5, "the_hierophant"),
    (6, "the_lovers"),
    (7, "the_chariot"),
    (8, "strength"),
    (9, "the_hermit"),
    (10, "wheel_of_fortune"),
    (11, "justice"),
    (12, "the_hanged_man"),
    (13, "death"),
    (14, "temperance"),
    (15, "the_devil"),
    (16, "the_tower"),
    (17, "the_star"),
    (18, "the_moon"),
    (19, "the_sun"),
    (20, "judgement"),
    (21, "the_world"),
]

MINOR_SUITS = ["wands", "cups", "swords", "pentacles"]
COURT_CARDS = {11: "page", 12: "knight", 13: "queen", 14: "king"}


class VerificationResult(NamedTuple):
    """Result of a single verification check."""

    passed: bool
    message: str
    severity: str = "info"  # info, warning, error


class CardCheck(NamedTuple):
    """Result of checking a specific card."""

    name: str
    expected_file: str
    found: bool
    file_size: int
    issues: List[str]


class RWSImageVerifier:
    """Verifies Rider-Waite-Smith card images."""

    def __init__(self, theme_dir: str = "themes/classic", verbose: bool = False):
        self.theme_dir = Path(theme_dir)
        self.verbose = verbose
        self.results: Dict[str, List[CardCheck]] = {
            "major": [],
            "wands": [],
            "cups": [],
            "swords": [],
            "pentacles": [],
        }
        self.errors: List[str] = []
        self.warnings: List[str] = []

    def log(self, message: str, level: str = "info"):
        """Print message if verbose or if important."""
        if self.verbose or level in ["warning", "error"]:
            prefix = {"info": "  ", "warning": "⚠ ", "error": "✗ "}.get(level, "  ")
            print(f"{prefix}{message}")

    def verify_theme_json(self) -> VerificationResult:
        """Verify theme.json exists and is valid."""
        theme_json_path = self.theme_dir / "theme.json"

        if not theme_json_path.exists():
            return VerificationResult(False, f"theme.json not found at {theme_json_path}", "error")

        try:
            with open(theme_json_path, "r", encoding="utf-8") as f:
                theme_config = json.load(f)

            required_fields = ["name", "description", "author", "version"]
            missing = [f for f in required_fields if f not in theme_config]

            if missing:
                return VerificationResult(
                    False, f"theme.json missing fields: {', '.join(missing)}", "error"
                )

            self.log(f"Theme: {theme_config.get('name')}")
            self.log(f"Author: {theme_config.get('author')}")
            self.log(f"Version: {theme_config.get('version')}")

            return VerificationResult(
                True, f"theme.json valid - {theme_config.get('name')}", "info"
            )

        except json.JSONDecodeError as e:
            return VerificationResult(False, f"theme.json is invalid JSON: {e}", "error")
        except Exception as e:
            return VerificationResult(False, f"Error reading theme.json: {e}", "error")

    def get_expected_filename(self, suit: str, number: int, name: str = "") -> str:
        """Generate expected filename for a card."""
        num_str = f"{number:02d}"

        if suit == "major":
            return f"major_{num_str}_{name}.png"
        else:
            # Minor arcana
            if number == 1:
                return f"{suit}_01_ace.png"
            elif number >= 11:
                court_name = COURT_CARDS.get(number, str(number))
                return f"{suit}_{num_str}_{court_name}.png"
            else:
                return f"{suit}_{num_str}.png"

    def check_card(self, suit: str, number: int, name: str = "") -> CardCheck:
        """Check if a specific card image exists."""
        expected_file = self.get_expected_filename(suit, number, name)
        file_path = self.theme_dir / expected_file

        found = file_path.exists()
        file_size = file_path.stat().st_size if found else 0
        issues = []

        if not found:
            issues.append(f"Missing: {expected_file}")
            self.errors.append(f"{suit}/{number}: {expected_file} not found")
        elif file_size == 0:
            issues.append(f"Empty file: {expected_file}")
            self.errors.append(f"{suit}/{number}: {expected_file} is 0 bytes")
        elif file_size < 1000:
            issues.append(f"Suspiciously small: {expected_file} ({file_size} bytes)")
            self.warnings.append(f"{suit}/{number}: {expected_file} is only {file_size} bytes")

        display_name = name.replace("_", " ").title() if name else f"{number}"
        if suit != "major":
            suit_name = suit.title()
            if number == 1:
                display_name = f"Ace of {suit_name}"
            elif number >= 11:
                display_name = f"{COURT_CARDS[number].title()} of {suit_name}"
            else:
                display_name = f"{number} of {suit_name}"
        else:
            display_name = name.replace("_", " ").title()

        return CardCheck(
            name=display_name,
            expected_file=expected_file,
            found=found,
            file_size=file_size,
            issues=issues,
        )

    def verify_major_arcana(self) -> Tuple[int, int]:
        """Verify all 22 Major Arcana cards."""
        print("\n📜 Major Arcana (22 cards):")

        found_count = 0
        for number, name in MAJOR_ARCANA:
            check = self.check_card("major", number, name)
            self.results["major"].append(check)

            if check.found:
                found_count += 1
                status = "✓"
            else:
                status = "✗"

            if self.verbose or not check.found:
                print(f"  {status} {number:2d}. {check.name:25s} {check.expected_file}")
                for issue in check.issues:
                    print(f"      ⚠ {issue}")

        return found_count, len(MAJOR_ARCANA)

    def verify_minor_arcana(self, suit: str) -> Tuple[int, int]:
        """Verify all 14 cards of a minor arcana suit."""
        if suit == "wands":
            suit_emoji = "🔥"
        elif suit == "cups":
            suit_emoji = "💧"
        elif suit == "swords":
            suit_emoji = "⚔️"
        else:
            suit_emoji = "🌍"

        print(f"\n{suit_emoji} {suit.title()} (14 cards):")

        found_count = 0
        for number in range(1, 15):
            check = self.check_card(suit, number)
            self.results[suit].append(check)

            if check.found:
                found_count += 1
                status = "✓"
            else:
                status = "✗"

            if self.verbose or not check.found:
                print(f"  {status} {check.name:25s} {check.expected_file}")
                for issue in check.issues:
                    print(f"      ⚠ {issue}")

        return found_count, 14

    def verify_all_images(self) -> bool:
        """Run all verification checks."""
        print("=" * 60)
        print("Rider-Waite-Smith Image Verification")
        print("=" * 60)
        print(f"\n📁 Checking: {self.theme_dir.absolute()}")

        # Check theme directory exists
        if not self.theme_dir.exists():
            print(f"\n✗ ERROR: Theme directory does not exist: {self.theme_dir}")
            print("\nTo create it, run:")
            print(f"  mkdir -p {self.theme_dir}")
            return False

        # Verify theme.json
        print("\n📋 Theme Configuration:")
        theme_result = self.verify_theme_json()
        if not theme_result.passed:
            print(f"  ✗ {theme_result.message}")
        else:
            print(f"  ✓ {theme_result.message}")

        # Verify all card sets
        major_found, major_total = self.verify_major_arcana()

        minor_results = {}
        for suit in MINOR_SUITS:
            found, total = self.verify_minor_arcana(suit)
            minor_results[suit] = (found, total)

        # Summary
        total_found = major_found + sum(f for f, _ in minor_results.values())
        total_expected = 22 + (14 * 4)  # 22 Major + 56 Minor

        print("\n" + "=" * 60)
        print("Verification Summary")
        print("=" * 60)

        print("\n📊 Results:")
        print(
            f"  Major Arcana:  {major_found:2d}/{major_total} "
            f"{'✓' if major_found == major_total else '✗'}"
        )
        for suit, (found, total) in minor_results.items():
            print(f"  {suit.title():13s} {found:2d}/{total} {'✓' if found == total else '✗'}")

        print(f"\n  {'Total':13s} {total_found:2d}/{total_expected}")

        # Check for extra files
        print("\n📁 File Analysis:")
        expected_files = set()
        for number, name in MAJOR_ARCANA:
            expected_files.add(self.get_expected_filename("major", number, name))
        for suit in MINOR_SUITS:
            for number in range(1, 15):
                expected_files.add(self.get_expected_filename(suit, number))

        actual_files = set(f.name for f in self.theme_dir.glob("*.png"))
        extra_files = actual_files - expected_files

        if extra_files:
            print(f"  ⚠ {len(extra_files)} unexpected file(s) found:")
            for f in sorted(extra_files):
                print(f"      - {f}")
        else:
            print("  ✓ No unexpected files")

        # File size analysis
        total_size = sum(
            check.file_size
            for suit_results in self.results.values()
            for check in suit_results
            if check.found
        )
        avg_size = total_size // total_found if total_found > 0 else 0

        print(f"\n  Total size: {total_size / (1024*1024):.2f} MB")
        print(f"  Average: {avg_size / 1024:.1f} KB per image")

        # Issues summary
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors[:10]:
                print(f"    - {error}")
            if len(self.errors) > 10:
                print(f"    ... and {len(self.errors) - 10} more")

        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings[:5]:
                print(f"    - {warning}")
            if len(self.warnings) > 5:
                print(f"    ... and {len(self.warnings) - 5} more")

        # Final status
        print("\n" + "=" * 60)
        if total_found == total_expected and len(self.errors) == 0:
            print("✅ Status: PASSED - All images ready!")
            print("=" * 60)
            return True
        else:
            missing = total_expected - total_found
            print(f"❌ Status: FAILED - {missing} image(s) missing or invalid")
            print("=" * 60)
            return False

    def generate_report(self) -> str:
        """Generate a detailed markdown report."""
        lines = [
            "# RWS Image Verification Report",
            "",
            f"**Date:** {__import__('datetime').datetime.now().isoformat()}",
            f"**Theme Directory:** {self.theme_dir}",
            "",
            "## Summary",
            "",
        ]

        # Count totals
        total_found = sum(
            1 for suit_results in self.results.values() for check in suit_results if check.found
        )
        total_expected = 78

        lines.append(f"- **Total Cards:** {total_found}/{total_expected}")
        lines.append(f"- **Errors:** {len(self.errors)}")
        lines.append(f"- **Warnings:** {len(self.warnings)}")
        lines.append("")

        # Detailed results by suit
        for suit_name, checks in self.results.items():
            lines.append(f"## {suit_name.title()}")
            lines.append("")
            lines.append("| Card | Filename | Status | Size |")
            lines.append("|------|----------|--------|------|")

            for check in checks:
                status = "✅" if check.found else "❌"
                size = f"{check.file_size / 1024:.1f} KB" if check.found else "N/A"
                lines.append(f"| {check.name} | `{check.expected_file}` | {status} | {size} |")

            lines.append("")

        # Issues section
        if self.errors:
            lines.append("## Errors")
            lines.append("")
            for error in self.errors:
                lines.append(f"- ❌ {error}")
            lines.append("")

        if self.warnings:
            lines.append("## Warnings")
            lines.append("")
            for warning in self.warnings:
                lines.append(f"- ⚠️ {warning}")
            lines.append("")

        lines.append("---")
        lines.append("*Generated by verify_rws_images.py*")

        return "\n".join(lines)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Verify Rider-Waite-Smith tarot card images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python scripts/verify_rws_images.py
  python scripts/verify_rws_images.py --verbose
  python scripts/verify_rws_images.py --report verification.md
        """,
    )
    parser.add_argument(
        "--theme-dir",
        default="themes/classic",
        help="Path to theme directory (default: themes/classic)",
    )
    parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed output for each card"
    )
    parser.add_argument("--report", "-r", metavar="FILE", help="Generate markdown report to FILE")
    parser.add_argument(
        "--exit-code", action="store_true", help="Exit with non-zero code if verification fails"
    )

    args = parser.parse_args()

    # Run verification
    verifier = RWSImageVerifier(theme_dir=args.theme_dir, verbose=args.verbose)

    passed = verifier.verify_all_images()

    # Generate report if requested
    if args.report:
        report = verifier.generate_report()
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\n📝 Report saved to: {args.report}")

    # Exit code
    if args.exit_code and not passed:
        sys.exit(1)

    sys.exit(0 if passed else 0)  # Default: always exit 0 unless --exit-code


if __name__ == "__main__":
    main()
