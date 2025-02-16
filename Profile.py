# Instructor-given code, however, reformatted to fit within pycodestyle requirements
# Author: Mark S. Baldwin, modified by Alberto Krone-Martins
#
# v0.1.9

# You should review this code to identify what features you need to support
# in your program for assignment 2.
#


import json
import time
from pathlib import Path


class DsuFileError(Exception):
    """
    DsuFileError is a custom exception handler that you should catch
    in your own code. It is raised when attempting to load or save
    Profile objects to the file system.
    """
    pass


class DsuProfileError(Exception):
    """
    DsuProfileError is a custom exception handler that you should catch
    in your own code. It is raised when attempting to deserialize
    a dsu file to a Profile object.
    """
    pass


class Post(dict):
    """
    The Post class is responsible for working with individual user posts.
    It supports two features: A timestamp property that is set upon
    instantiation and when the entry object is set, and an entry property
    that stores the post message.
    """

    def __init__(self, entry: str = None, timestamp: float = 0):
        self._timestamp = timestamp
        self.set_entry(entry)

        # Subclass dict to expose Post properties for serialization
        dict.__init__(self, entry=self._entry, timestamp=self._timestamp)

    def set_entry(self, entry):
        self._entry = entry
        dict.__setitem__(self, 'entry', entry)

        # If timestamp has not been set, generate a new one from time module
        if self._timestamp == 0:
            self._timestamp = time.time()

    def get_entry(self):
        return self._entry

    def set_time(self, time_value: float):
        self._timestamp = time_value
        dict.__setitem__(self, 'timestamp', time_value)

    def get_time(self):
        return self._timestamp

    # Property methods for entry and timestamp
    entry = property(get_entry, set_entry)
    timestamp = property(get_time, set_time)


class Profile:
    """
    The Profile class manages user information for the journal system.
    It ensures that username and password are set and allows adding,
    deleting, and retrieving posts.
    """

    def __init__(self, dsuserver=None, username=None, password=None):
        self.dsuserver = dsuserver  # REQUIRED
        self.username = username  # REQUIRED
        self.password = password  # REQUIRED
        self.bio = ''  # OPTIONAL
        self._posts = []  # OPTIONAL

    def add_post(self, post: Post) -> None:
        """
        Accepts a Post object and appends it to the posts list.
        Posts are stored in the order they are added.
        """
        self._posts.append(post)

    def del_post(self, index: int) -> bool:
        """
        Removes a Post at a given index and returns True if successful,
        False if an invalid index was supplied.
        """
        try:
            del self._posts[index]
            return True
        except IndexError:
            return False

    def get_posts(self) -> list:
        """
        Returns the list object containing all posts added to the Profile.
        """
        return self._posts

    def save_profile(self, path: str) -> None:
        """
        Saves the current instance of Profile to a DSU file.

        Example usage:
        profile = Profile()
        profile.save_profile('/path/to/file.dsu')

        Raises DsuFileError.
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'w') as f:
                    json.dump(self.__dict__, f)
            except Exception as ex:
                raise DsuFileError(
                    "Error while attempting to process the DSU file.", ex
                )
        else:
            raise DsuFileError("Invalid DSU file path or type")

    def load_profile(self, path: str) -> None:
        """
        Populates the current instance of Profile with data from a DSU file.

        Example usage:
        profile = Profile()
        profile.load_profile('/path/to/file.dsu')

        Raises DsuProfileError, DsuFileError.
        """
        p = Path(path)

        if p.exists() and p.suffix == '.dsu':
            try:
                with open(p, 'r') as f:
                    obj = json.load(f)
                    self.username = obj['username']
                    self.password = obj['password']
                    self.dsuserver = obj['dsuserver']
                    self.bio = obj['bio']
                    self._posts = [
                        Post(post_obj['entry'], post_obj['timestamp'])
                        for post_obj in obj['_posts']
                    ]
            except Exception as ex:
                raise DsuProfileError(ex)
        else:
            raise DsuFileError()
