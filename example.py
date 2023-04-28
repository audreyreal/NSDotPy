# This file is part of NSDotPy, a wrapper around requests that makes interacting with the HTML nationstates.net site legally and efficiently easier.
#
# NSDotPy is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# NSDotPy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with NSDotPy. If not, see <https://www.gnu.org/licenses/>.


# This example is a souped-up prepping script, it will apply to the WA,
# move to a region of your choice, as well as change the nation's flag and fields
# for all nations in the config.toml or config.json file
import os, json
import rtoml  # for config file
from src.session import NSSession


def handle_config_files():
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
            "nations": {f"nation {i}": "password" for i in range(5)},
        }
        rtoml.dump(template, open("config.toml", "w"))
        print(
            "No config file found, created one. Please edit it and run the script again."
        )
        exit()
    return config


def main():
    # read config file, create one if it doesn't exist
    config = handle_config_files()

    # initialize session
    session = NSSession("Prepping helper", "1.0.0", "Sweeze", config["main_nation"])
    # bring the config file into memory
    nations = config["nations"]

    # loop through all nations in config file
    for nation, password in nations:
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
            session.move_to_region(config["jump_point"])


if __name__ == "__main__":
    main()
