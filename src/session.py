# This file is part of NSDotPy, a wrapper around requests that makes interacting with the HTML nationstates.net site legally and efficiently easier.
#
# NSDotPy is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License
# as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
#
# NSDotPy is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License along with NSDotPy. If not, see <https://www.gnu.org/licenses/>.

import time # for ratelimiting and userclick

import keyboard # for the required user input
import requests # for http stuff
from tendo.singleton import SingleInstance # so it can only be run once at a time
from bs4 import BeautifulSoup # for parsing html and xml

def canonicalize(string: str) -> str:
    """Converts a string to its canonical form used by the nationstates api.

    Args:
        string (str): The string to convert

    Returns:
        str: The canonical form of the string
    """
    return string.lower().strip().replace(" ", "_")


class NSSession:
    def __init__(self, script_name: str, script_version: str, script_author: str, script_user: str, keybind: str = "space", link_to_src: str = ""):
        """A wrapper around requests that abstracts away interacting with the HTML nationstates.net site.
        Focused on legality, correctness, and ease of use.

        Args:
            script_name (str): Name of your script
            script_version (str): Version number of your script
            script_author (str): Author of your script
            script_user (str): Nation name of the user running your script
            keybind (str, defaults to space): Keybind to fulfill one click = one request rule
            link_to_src (str, optional): Link to the source code of your script.
        """
        self.VERSION = "1.0.0"
        # Attach the tendo singleton to the session object so it can only be run once at a time, avoiding simultaneity issues
        self._me = SingleInstance()
        # Create a new requests session
        self._session = requests.Session()
        # Set the user agent to the script name, version, author, and user as recommended in the script rules thread:
        # https://forum.nationstates.net/viewtopic.php?p=16394966&sid=be37623536dbc8cee42d8d043945b887#p16394966
        self.user_agent = f"{script_name}/{script_version} (by:{script_author}; usedBy:{script_user})"
        if link_to_src:
            self.user_agent = f"{self.user_agent}; src:{link_to_src}"
        self.user_agent = f"{self.user_agent}; Written with NSDotPy/{self.VERSION} (by:Sweeze; src:github.com/sw33ze/NSDotPy)"
        self._session.headers.update({"User-Agent": self.user_agent})
        # If a link to the source code is provided, add it to the user agent
        # Initialize nationstates specific stuff
        self.chk: str = ""
        self.localid: str = ""
        self.pin: str = ""
        self.current_nation: str = ""
        self.current_region: str = ""
        print(f"Initialized. Keybind to continue is {keybind}.")

    def _get_auth_values(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        # gathering chk and localid so i dont have to worry about authenticating l8r
        if chk := soup.find("input", {"name": "chk"}):
            self.chk = chk["value"].strip() # type: ignore
        if localid := soup.find("input", {"name": "localid"}):
            self.localid = localid["value"].strip() # type: ignore
        if pin := self._session.cookies.get("pin"):
            # you should never really need the pin but just in case i'll store it
            self.pin = pin
        if soup.find("div", {"id": "panel"}):
            self.current_region = canonicalize(soup.find_all("a", {"class": "STANDOUT"})[1].text)

    def _wait_for_input(self, key: str) -> int:
        """Blocks execution until the user presses a key. Used as the one click = one request action.
        
        Args:
            key (str): The key to wait for
        
        Returns:
            int: Userclick parameter, milliseconds since the epoch"""
        keyboard.wait(key)
        # trigger_on_release is broken because of a bug in keyboard so we have to do this
        while keyboard.is_pressed(key):
            pass
        return int(time.time() * 1000)

    def _validate_fields(self, data: dict):
        max_lengths = {
            "pretitle": 28,
            "slogan": 55,
            "currency": 40,
            "animal": 40,
            "demonym_noun": 44,
            "demonym_adjective": 44,
            "demonym_plural": 44
        }

        # go through each key in the data dict and make sure they're below the max length
        for key, value in data.items():
            if len(value) > max_lengths[key]:
                raise ValueError(f"{key} is too long, max length is {max_lengths[key]}")
            if len(value) < 2 and key != 'slogan':
                raise ValueError(f"{key} should have a minimum length of 2 characters.")
            # check if pretitle contains any non-alphanumeric characters (except spaces)
            if key == "pretitle" and not value.replace(" ", "").isalnum():
                raise ValueError("Pretitle should only contain alphanumeric characters.")

    # --- end private methods --- #

    def request(self, url: str, data: dict = {}, files: dict = {}, allow_redirects: bool = False) -> requests.Response:
        """Sends a request to the given url with the given data and files.

        Args:
            url (str): URL to send the request to
            data (dict, optional): Payload to send with the request
            files (dict, optional): Payload to send with requests that upload files

        Returns:
            requests.Response: The response from the server
        """
        if any(banned_page in canonicalize(url) for banned_page in ["page=telegrams", "page=dilemmas"]):
            raise ValueError("You cannot use a tool to interact with telegrams or dilemmas. Read up on the script rules: https://forum.nationstates.net/viewtopic.php?p=16394966#p16394966")
        elif "api.cgi" in canonicalize(url):
            # deal with ratelimiting if its an api request
            return self.api_request(data)
        elif "nationstates.net" not in canonicalize(url):
            # if its not nationstates then just pass the request through
            return self._session.post(url, data=data, allow_redirects=allow_redirects)
        else:
            # there's no reason to be adding chk and localid if we're logging in
            if "region=rwby" not in url:
                data |= {"chk": self.chk, "localid": self.localid}
            userclick = self._wait_for_input("space")
            # userclick is the number of milliseconds since the epoch, admin uses this for help enforcing the simultaneity rule
            response = self._session.post(f"{url}/userclick={userclick}", data=data, files=files, allow_redirects=allow_redirects)
            self._get_auth_values(response)
            # you should never need the pin explicitly, but its here just in case
            return response

    def api_request(self, data: dict) -> requests.Response:
        """Sends a request to the nationstates api with the given data.

        Args:
            data (dict): Payload to send with the request, e.g. {"nation": "testlandia", "q": "region"}

        Returns:
            requests.Response: The response from the server
        """
        # TODO: probably move this responsibility to a third party api library to avoid reinventing the wheel
        # if one exists of sufficient quality thats AGPLv3 compatible
        data |= {"v": "12"}
        # rate limiting section
        response = self._session.post("https://www.nationstates.net/cgi-bin/api.cgi", data=data)
        # if the server tells us to wait, wait
        head = response.headers
        if waiting_time := head.get("Retry-After"):
            print(f"Rate limited. Waiting {waiting_time} seconds.")
            time.sleep(int(waiting_time))
        # slow down requests so we dont hit the rate limit in the first place
        requests_left = int(head["X-RateLimit-Remaining"])
        seconds_until_reset = int(head["X-RateLimit-Reset"])
        time.sleep(seconds_until_reset / requests_left)
        # end rate limiting section
        return response

    def login(self, nation: str, password: str) -> bool:
        """Logs in to the nationstates site.

        Args:
            nation (str): Nation name
            password (str): Nation password

        Returns:
            bool: True if login was successful, False otherwise
        """
        print(f"Logging in to {nation}")
        url = "https://century.nationstates.net/page=display_region/region=rwby"
        # shoutouts to roavin for telling me i had to have page=display_region in the url so it'd work with a userclick parameter

        data = {
            "nation": canonicalize(nation),
            "password": password,
            "logging_in": "1",
            "submit": "Login"
        }

        response = self.request(url, data)

        soup = BeautifulSoup(response.text, "html.parser")
        # checks if the body tag has your nation name in it; if it does, you're logged in
        if not soup.find("body", {"data-nname": canonicalize(nation)}):
            return False

        self.current_nation = canonicalize(nation)
        return True

    def change_nation_flag(self, flag_filename: str) -> bool:
        """Changes the nation flag to the given image.

        Args:
            flag_filename (str): Filename of the flag to change to

        Returns:
            bool: True if the flag was changed, False otherwise
        """
        print("Changing nation flag")
        # THIS WAS SO FUCKING FRUSTRATING BUT IT WORKS NOW AND IM NEVER TOUCHING THIS BULLSHIT UNLESS NS BREAKS IT AGAIN
        url = "https://www.nationstates.net/cgi-bin/upload.cgi"

        data = {
            "nationname": self.current_nation,
        }
        files = {
            "file": (flag_filename, open(flag_filename, "rb"), f"image/{flag_filename.lower().split('.')[-1]}")
        }

        response = self.request(url, data=data, files=files)

        if response.headers.get("location") == "https://www.nationstates.net/page=settings":
            return True
        elif "Just a moment..." in response.text:
            print("Cloudflare blocked you idiot get fucked have fun with that like I had to lmaoooooooooo")
        return False

    def change_nation_settings(
            self,
            *,
            email: str = "",
            pretitle: str = "",
            slogan: str = "",
            currency: str = "",
            animal: str = "",
            demonym_noun: str = "",
            demonym_adjective: str = "",
            demonym_plural: str = "",
            new_password: str = "",
        ) -> bool:
        """Given a logged in session, changes customizable fields and settings of the logged in nation.
        Variables must be explicitly named in the call to the function, e.g. "session.change_nation_settings(pretitle='Join Lily', currency='Join Lily')"

        Args:
            email (str, optional): New email for WA apps.
            pretitle (str, optional): New pretitle of the nation. Max length of 28.
            slogan (str, optional): New Slogan/Motto of the nation. Max length of 55.
            currency (str, optional): New currency of the nation. Max length of 40.
            animal (str, optional): New national animal of the nation. Max length of 40.
            demonym_noun (str, optional): Noun the nation will refer to its citizens as. Max length of 44.
            demonym_adjective (str, optional): Adjective the nation will refer to its citizens as. Max length of 44.
            demonym_plural (str, optional): Plural form of "demonym_noun". Max length of 44.
            new_password (str, optional): New password to assign to the nation.

        Returns:
            bool: True if changes were successful, False otherwise.
        """
        print("Changing nation settings")
        url = "https://www.nationstates.net/template-overall=none/page=settings"

        data = {
            "type": pretitle,
            "slogan": slogan,
            "currency": currency,
            "animal": animal,
            "demonym2": demonym_noun,
            "demonym": demonym_adjective,
            "demonym2pl": demonym_plural,
            "email": email,
            "password": new_password,
            "confirm_password": new_password,
            "update": " Update ",
        }
        # remove keys that have empty values
        data = {k: v for k, v in data.items() if v}
        # make sure everything is following the proper length limits and only contains acceptable characters
        self._validate_fields(data)

        response = self.request(url, data)
        return "Your settings have been successfully updated." in response.text
    
    def move_to_region(self, region: str, password: str = "") -> bool:
        """Moves the nation to the given region.

        Args:
            region (str): Region to move to
            password (str, optional): Region password, if the region is passworded

        Returns:
            bool: True if the move was successful, False otherwise
        """
        print(f"Moving to {region}")
        url = "https://www.nationstates.net/template-overall=none/page=change_region"

        data = {
            "region_name": region,
            "move_region": "1"
        }
        if password:
            data["password"] = password
        response = self.request(url, data)

        if "Success!" in response.text:
            self.current_region = canonicalize(region)
            return True
        return False
    
    def vote(self, pollid: str, option: str) -> bool:
        """Votes on a poll.

        Args:
            pollid (str): ID of the poll to vote on, e.g. "199747"
            option (str): Option to vote for (starts at 0)

        Returns:
            bool: True if the vote was successful, False otherwise
        """
        print(f"Voting on poll {pollid}")
        url = f"https://www.nationstates.net/template-overall=none/page=poll/p={pollid}"

        data = {
            "pollid": pollid,
            "q1": option,
            "poll_submit": "1"
        }
        response = self.request(url, data)

        return "Your vote has been lodged." in response.text
    
    def join_wa(self, nation: str, app_id: str) -> bool:
        """Joins the WA with the given nation.

        Args:
            nation (str): Nation to join the WA with
            app_id (str): ID of the WA application to use

        Returns:
            bool: True if the join was successful, False otherwise
        """
        print(f"Joining WA with {nation}")
        url = "https://www.nationstates.net/cgi-bin/join_un.cgi"

        data = {
            "nation": canonicalize(nation),
            "appid": app_id
        }
        response = self.request(url, data)

        if status := response.headers.get("location") == "https://www.nationstates.net/page=un?welcome=1":
            # since we're just getting thrown into a cgi script, we'll have to manually grab authentication values
            self.request("https://century.nationstates.net/page=display_region/region=rwby")
        return status

    def resign_wa(self):
        """Resigns from the WA.

        Returns:
            bool: True if the resignation was successful, False otherwise
        """
        print("Resigning from WA")
        url = "https://www.nationstates.net/template-overall=none/page=UN_status"

        data = {
            "action": "leave_UN",
            "submit": "1"
        }
        response = self.request(url, data)

        return "From this moment forward, your nation is on its own." in response.text

    def apply_wa(self, reapply: bool = True) -> bool:
        """Applies to the WA.

        Args:
            reapply (bool, optional): Whether to reapply if you've been sent an application that's still valid. Defaults to True.

        Returns:
            bool: True if the application was successful, False otherwise
        """
        print("Applying to WA")
        url = "https://www.nationstates.net/template-overall=none/page=UN_status"

        data = {
            "action": "join_UN"
        }
        if reapply:
            data["resend"] = "1"
        else:
            data["submit"] = "1"

        response = self.request(url, data)
        return "Your application to join the World Assembly has been received!" in response.text

    def endorse(self, nation: str, endorse: bool = True) -> bool:
        """Endorses the given nation.

        Args:
            nation (str): Nation to endorse
            endorse (bool, optional): True=endorse, False=unendorse. Defaults to True.

        Returns:
            bool: True if the endorsement was successful, False otherwise
        """
        print(f"Endorsing {nation}")
        url = "https://www.nationstates.net/cgi-bin/endorse.cgi"

        data = {
            "nation": canonicalize(nation),
            "action": "endorse" if endorse else "unendorse"
        }
        response = self.request(url, data)

        return (
            response.headers.get("location")
            == f"https://www.nationstates.net/nation={canonicalize(nation)}"
        )
    
    def clear_dossier(self) -> bool:
        """Clears a logged in nation's dossier.

        Returns:
            bool: Whether it was successful or not
        """

        print("Clearing dossier")
        url = "https://www.nationstates.net/template-overall=none/page=dossier"
        data = {
            "clear_dossier": "1"
        }
        response = self.request(url, data)

        return "Dossier cleared of nations." in response.text

    def wa_vote(self, council: str, vote: str) -> bool:
        """Votes on the current WA resolution.

        Args:
            council (str): Must be "ga" for general assembly, "sc" for security council.
            vote (str): Must be "for" or "against".

        Returns:
            bool: Whether the vote was successful or not
        """

        if council not in ["ga", "sc"]:
            raise ValueError("council must be 'ga' or 'sc'")
        if vote not in ["for", "against"]:
            raise ValueError("vote must be 'for' or 'against'")
        print("Voting on WA resolution")

        url = f"https://www.nationstates.net/template-overall=none/page={council}"
        data = {
            "vote": f"Vote+{vote.capitalize()}",
        }
        response = self.request(url, data)

        return "Your vote has been lodged." in response.text

if __name__ == "__main__":
    print("this is a module, not a script")
