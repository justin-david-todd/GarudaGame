# Author: Justin David Todd
# Last Modified: 02/02/2021
# Description: This System class represents the running game console.
#   Holds system's "ON" status and stores/retrieves game saves, high scores, etc.


class System:
    """Holds system's ON status and stores and retrieves game saves."""

    def __init__(self):
        """Initializes attributes that store game running and save data"""
        self._system_on = True

    def on(self):
        """Returns True if the system is On, else False"""
        return self._system_on

    def off(self):
        """Turns the system off"""
        self._system_on = False
