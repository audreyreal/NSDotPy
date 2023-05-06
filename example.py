# This file is part of NSDotPy, a wrapper around requests that makes interacting
# with the HTML nationstates.net site legally and efficiently easier.
#
# NSDotPy is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation either version
# 3 of the License, or (at your option) any later version.
#
# NSDotPy is distributed in the hope that it will be useful but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with NSDotPy. If not, see <https://www.gnu.org/licenses/>.


# This example is a souped-up prepping script, it will apply to the WA,
# move to a region of your choice, as well as change the nation's flag and fields
# for all nations in a config.toml or config.json file

import os  # swarm config file
import json  # for checking if config file exists
import rtoml  # for config file
from src.session import NSSession  # for interacting with nationstates


def handle_config_files() -> dict[str, str | dict[str, str]]:
    if os.path.exists("config.toml"):
        # load config file
        config = rtoml.load(open("config.toml", "r"))
        if config["main_nation"] == "Your Main Nation Here":
            print("Please actually fill in config file and run the script again.")
            exit()
    elif os.path.exists("config.json"):
        # load alternative config file
        config = json.load(open("config.json", "r"))
    else:
        # no config file, create one
        template = {
            "main_nation": "Your Main Nation Here",  # for user agent
            "jump_point": "The Allied Nations of Egalaria",  # for moving to
            "nations": {f"nation {i}": "password" for i in range(1, 6)},
        }
        rtoml.dump(template, open("config.toml", "w"))
        print(
            "No config file found, created one. Please edit it and run the script again."
        )
        exit()
    return config


def main() -> None:
    # read config file, create one if it doesn't exist
    config = handle_config_files()
    main: str = config["main_nation"]  # type: ignore
    # initialize session
    session = NSSession("Prepping helper", "1.0.1", "Sweeze", main)

    # loop through all nations in config file
    prep_nations(config, session)


def prep_nations(config: dict[str, str | dict[str, str]], session: NSSession) -> None:
    nations: dict[str, str] = config["nations"]  # type: ignore
    jp: str = config["jump_point"]  # type: ignore

    for nation, password in nations.items():
        # login to nation, move on to the next if login fails
        if session.login(nation, password):
            session.change_nation_flag("gif.gif")
            session.change_nation_settings(
                pretitle="Join Lily",  # do note this requires at least 250m population
                slogan="Join Lily",
                animal="Join Lily",
                currency="Join Lily",
            )
            session.apply_wa()
            session.move_to_region(jp)


if __name__ == "__main__":
    main()
