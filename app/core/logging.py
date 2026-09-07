import logging


def configure_logging(level: str = "INFO") -> None:
    """Configure predictable, secret-free console logging for the runtime."""
    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        force=True,
    )
