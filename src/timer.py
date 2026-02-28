
import time


def timer(minutes: int) -> None:
    """
    Runs a countdown timer.

    Args:
        minutes (int): Duration of the timer in minutes.
    """
    total_seconds = minutes * 60

    while total_seconds > 0:
        remaining_minutes, remaining_seconds = divmod(total_seconds, 60)

        print(f"{remaining_minutes:02d}:{remaining_seconds:02d}")

        time.sleep(1)
        total_seconds -= 1
