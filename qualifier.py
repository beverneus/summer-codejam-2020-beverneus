"""
Use this file to write your solution for the Summer Code Jam 2020 Qualifier.

Important notes for submission:

- Do not change the names of the two classes included below. The test suite we
  will use to test your submission relies on existence these two classes.

- You can leave the `ArticleField` class as-is if you do not wish to tackle the
  advanced requirements.

- Do not include "debug"-code in your submission. This means that you should
  remove all debug prints and other debug statements before you submit your
  solution.
"""
import datetime
import typing
import re
import itertools


class ArticleField:
    """Checks if assigned value has the correct type,
       raises a TypeError if it doesn't"""

    def __init__(self, field_type: typing.Type[typing.Any]):
        self.type = field_type

    def __get__(self, obj, type=None):
        try:
            return obj.__dict__.get(self.name)
        except NameError:
            return 0

    def __set__(self, obj, value):
        if not isinstance(value, self.type):
            raise TypeError(
                f"expected an instance of type {str(self.type)[7:-1]} for attribute '{self.name}', got {str(type(value))[7:-1]} instead")
        else:
            obj.__dict__[self.name] = value

    def __set_name__(self, owner, name):
        self.name = name


class Article:
    """The `Article` class you need to write for the qualifier."""

    id = 0

    def __init__(self, title: str, author: str, publication_date:
                 datetime.datetime, content: str):
        self.title = title
        self.author = author
        self.publication_date = publication_date
        self.content = content
        self.id = Article.id
        self.last_edited = None
        Article.id += 1

##########################
    # BASIC REQUIREMENTS
##########################

    def __repr__(self):
        return f"<Article title=\"{self.title}\" author=\'{self.author}\' publication_date=\'{str(self.publication_date).replace(' ', 'T')}\'>"

    def __len__(self):
        return len(self.content)

    def short_introduction(self, n_characters: int):
        cutpoints = [" ", "\n"]  # define characters for short intro end
        # give a number to every character and loop
        for character in enumerate(self.content[n_characters::-1]):
            if character[1] in cutpoints:
                return self.content[:n_characters-character[0]]
        # excecutes if no cutpoint is found
        else:
            return self.content[:n_characters]

    def most_common_words(self, n_words: int):
        used = {}
        # split sentence on non alphabet characters and loop through list
        for word in re.split('[^a-zA-Z]', self.content):
            if word.lower() in used:  # check if string is already in the dict
                used[word.lower()] += 1
            elif len(word) > 0:  # avoid putting an empty string in the dict
                used[word.lower()] = 1
        # sort the list and take the top n_words entries
        return dict(itertools.islice({key: value for key, value in sorted(
                                     used.items(), key=lambda item: item[1],
                                     reverse=True)}.items(), n_words))

#######################################
    # INTERMEDIATE REQUIREMENTS
#######################################

# executes when reading content
    @property
    def content(self):
        return self._content

# executes when reading content
    @content.setter
    def content(self, value):
        self._content = value
        self.last_edited = datetime.datetime.now()

# adds support for sorting instances fsfqs
    def __lt__(self, other):
        return self.publication_date < other.publication_date
