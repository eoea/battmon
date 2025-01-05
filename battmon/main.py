import math
import psutil
from enum import Enum
from mac_notifications import client

# Constants for battery percentage.
MAX: int = 80
MIN: int = 20


class Msg(Enum):
    title = 0
    subtitle = 1


def main() -> None:
    battery: psutil._common.sbattery = psutil.sensors_battery()

    suggest_disconnect_charger: list[str] = [
        f"Battery is at {battery.percent}%",
        "Disconnect the charger.",
    ]

    suggest_connect_charger: list[str] = [
        f"Battery is at {battery.percent}%",
        "Connect the charger.",
    ]

    if battery.power_plugged and battery.percent >= MAX:
        client.create_notification(
            title=suggest_disconnect_charger[Msg.title.value],
            subtitle=suggest_disconnect_charger[Msg.subtitle.value],
            action_button_str="OK",
        )
    if not battery.power_plugged and battery.percent <= MIN:
        # This check is needed because the battery seconds remaining is a
        # negative number when the battery remaining is not properly estimated.
        if battery.secsleft >= 0:
            hours_left: int = math.floor(battery.secsleft / 60 / 60)
            suggest_connect_charger[Msg.subtitle.value] = (
                suggest_connect_charger[Msg.subtitle.value]
                + " "
                + str(hours_left)
                + " hrs left."
            )
        client.create_notification(
            title=suggest_connect_charger[Msg.title.value],
            subtitle=suggest_connect_charger[Msg.subtitle.value],
            action_button_str="OK",
        )
