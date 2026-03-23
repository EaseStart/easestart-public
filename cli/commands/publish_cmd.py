#!/usr/bin/env python3
"""
EaseStart CLI — publish command

Publish marketing content to Facebook Page and Threads.
Preview → Confirm → Schedule (golden hour) → Publish → Log.
"""

import sys
from pathlib import Path

# Add project root to path for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def run_publish(args):
    """Execute the publish command."""
    # Load .env
    try:
        from dotenv import load_dotenv
        env_path = PROJECT_ROOT / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        else:
            load_dotenv()  # Try default locations
    except ImportError:
        pass  # dotenv optional; user can export vars manually

    from scripts.publish import ContentParser, MetaPublisher

    filepath = args.file
    if not Path(filepath).exists():
        # Try relative to project root
        alt = PROJECT_ROOT / filepath
        if alt.exists():
            filepath = str(alt)
        else:
            print(f"❌ File not found: {args.file}")
            sys.exit(1)

    # Parse content
    if filepath.endswith(".md"):
        content = ContentParser.parse_markdown(filepath)
    elif filepath.endswith(".txt"):
        content = ContentParser.parse_txt(filepath)
    else:
        print(f"❌ Unsupported file type: {filepath}")
        print("   Supported: .md, .txt")
        sys.exit(1)

    # Override media if provided via CLI
    if args.media:
        media_path = Path(args.media)
        if not media_path.exists():
            alt_media = Path(filepath).parent / args.media
            if alt_media.exists():
                media_path = alt_media
            else:
                print(f"❌ Media file not found: {args.media}")
                sys.exit(1)
        content["media"] = str(media_path)
        ext = media_path.suffix.lower()
        content["media_type"] = "video" if ext in (".mp4", ".mov", ".avi", ".webm") else "image"

    # Resolve carousel images
    image_paths = None
    if hasattr(args, "images") and args.images:
        image_paths = []
        for img in args.images:
            p = Path(img)
            if not p.exists():
                alt = Path(filepath).parent / img
                if alt.exists():
                    p = alt
                else:
                    print(f"❌ Image not found: {img}")
                    sys.exit(1)
            image_paths.append(str(p))

    # Determine platforms
    platforms = ["facebook", "threads"] if args.platform == "all" else [args.platform]

    publisher = MetaPublisher()
    results = {}

    for platform in platforms:
        print(f"\n{'═' * 60}")
        print(f"  📤 {platform.upper()}")
        print(f"{'═' * 60}")

        result = publisher.publish(
            platform=platform,
            content=content,
            post_now=args.now,
            dry_run=args.dry_run,
            skip_confirm=args.yes,
            image_paths=image_paths,
        )
        results[platform] = result

    # Summary
    print(f"\n{'═' * 60}")
    print("  📊 PUBLISH SUMMARY")
    print(f"{'═' * 60}")
    for platform, result in results.items():
        if result:
            status = f"✅ Published → {result.get('url', 'N/A')}"
        elif args.dry_run:
            status = "🔍 Dry run (not published)"
        else:
            status = "❌ Not published"
        print(f"  {platform.capitalize():10s} {status}")
    print()
