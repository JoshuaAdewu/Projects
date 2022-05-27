from django.db.models import DecimalField, ManyToManyField, BooleanField, ImageField, TextField, CharField, ForeignKey, \
    Model, CASCADE, EmailField

from re import fullmatch, Match
from validators import url

from django.db import models
from managetags.models import Tag
from typing import Any, Dict
import uuid


class User(Model):
    username: CharField = CharField(max_length=200)
    password: CharField = CharField(max_length=512)
    email: EmailField = EmailField(max_length=254, unique=False, default='ojjosh55@gmail.com')
    display_name: CharField = CharField(max_length=200)
    mature: BooleanField = BooleanField(default=False)
    user_blurb = models.CharField(max_length=1000, default="")
    admin = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    def is_valid_username(self) -> bool:
        """
        Returns True if self.username consists of only the following:
        Unicode word characters, numbers, hyphens, underscores.
        Also, the length of self.username must be >= 5 and <= 14
        """
        # strip to remove leading/trailing spaces
        stripped_uname: str = self.username.strip()

        # \w   : Unicode word chars, numbers
        # (-_): Hyphens, underscores
        # *    : Any number of times, 0 inclusive
        PATTERN: str = r"[\w(-_)]*"
        regex_match: Match = fullmatch(PATTERN, stripped_uname)

        # fullmatch returns a Match object if the string matches the pattern
        # otherwise, it returns None
        return (5 <= len(self.username) <= 14) and regex_match != None

    def is_unique_username(self) -> bool:
        """
        Returns True if self.username is not associated with another
        User in the database.
        """
        # DoesNotExist should be raised if the query returns nothing
        # TODO: come back, I may be misinterpreting queries
        try:
            User.objects.get(username=self.username)
        except self.DoesNotExist:
            return True
        return False

    def is_valid_display_name(self) -> bool:
        """
        Returns True if self.display_name has a length of >= 5 and <= 20.
        """
        return 5 <= len(self.display_name) <= 20

    def is_mature(self) -> bool:
        """
        Returns True if self.mature is True.
        """
        return self.is_mature

    def post_node(self, contentDict) -> str:
        """
        Returns True if node is posted correctly.
        contentDict contains:
            "node_title" -> CharField
            "node_content" -> CharField
            "image_file" -> ImageField
            "image_url" -> CharField
            "main_tag_id" -> IntegerField
            "mature_node" -> Bool (true when mature)
            "latitude" -> DecimalField
            "longitude" -> DecimalField
        """

        # Add title, content, and author to a new Node to insert
        node_args: Dict[str, Any] = {
            "node_title": contentDict["node_title"],
            "node_content": contentDict["node_content"],
            "node_author": self,
            "latitude": contentDict["latitude"],
            "longitude": contentDict["longitude"],
        }

        newNode: Node = Node(**node_args)

        # Check title and content for validity
        if not newNode.is_valid_title():
            return "Invalid title"
        if not newNode.is_valid_content():
            return "Content is limited to 10,000 characters"
        # Add image to node (if present) and check validity
        is_not_one_image = contentDict["image_file"] is not None and contentDict["image_url"] is not None
        is_image_not_added = False
        if not newNode.add_image(newURL=contentDict["image_url"]):
            if not newNode.add_image(newFile=contentDict["image_file"]):
                is_image_not_added = True
        if is_not_one_image:
            return "Invalid Image. You may add one image to each story."
        newNode.save()  # Every return after this MUST delete newNode, it was saved to create its id for ManyToMany
        # Add main tag to story and validate that it exists
        if (not Tag.objects.count()) or (int(contentDict["main_tag_id"]) < 0) or (
        not newNode.attach_main_tag(Tag.objects.get(id=int(contentDict["main_tag_id"])).add_tag_to_node())):
            newNode.delete()
            return "Main Tag not found. Please select a valid main tag."
        # Add mature rating is node contains mature content
        if contentDict["mature_node"]:
            newNode.attach_mature_tag()
        # Verify longitude and latitude
        MAX_LONG = 180
        MIN_LONG = -180
        MAX_LAT = 90
        MIN_LAT = -90
        if not (float(contentDict["latitude"]) <= MAX_LAT and float(contentDict["latitude"]) >= MIN_LAT):
            newNode.delete()
            return "Invalid latitude"
        elif not (float(contentDict["longitude"]) <= MAX_LONG and float(contentDict["longitude"]) >= MIN_LONG):
            newNode.delete()
            return "Invalid longitude"

        # Now that everything has been verified. The node can be successfully
        # saved to the database and the user can receive a success message.
        newNode.save()
        newNode.generate_id()
        newNode.save()

        return "Successfully Added your Story! Please refresh page to see changes."

    def unique_email(self) -> bool:
        try:
            User.objects.get(email=self.email)
        except self.DoesNotExist:
            return True
        return False

class Ban(models.Model):
    # the id of the user who put in the report (set null so we can keep the reports)
    bannedUser = models.CharField(max_length=200)

    def __str__(self):
        return self.bannedUser


class Node(Model):
    """ Story Node class. Holds a story's contents to present
    to users that select the respective story node. """
    image: ImageField = ImageField(upload_to="storyimages",
                                   default=None)  # File for an image if a file is given by user
    post_id: CharField = CharField(max_length=200, default="")
    image_url: TextField = TextField()  # URL to source an image from if URL is given by user
    node_title: CharField = CharField(max_length=200)  # Title of the story stored in the Node
    node_content: CharField = CharField(max_length=10_000)  # Story content (text) of node
    # The Node has an url if False, otherwise it has an image file
    has_image_file: BooleanField = BooleanField(default=False)  # True only when user gave a file for an image
    # Node coordinates on map
    longitude: DecimalField = DecimalField(max_digits=25, decimal_places=21, null=True)
    latitude: DecimalField = DecimalField(max_digits=25, decimal_places=21, null=True)
    node_author: ForeignKey = ForeignKey(User, on_delete=CASCADE, null=True)  # Account/user who created the Node
    main_tag_id: int = 0  # Primary story content Tag's id. One main Tag can relate to many story Nodes.
    other_tags: ManyToManyField = ManyToManyField(Tag, blank=True)  # A Node can have many tags for further filtering

    def __str__(self):
        """
        Returns current Title for A Story Node.
        """
        return self.node_title

    def is_valid_title(self) -> bool:
        """
        The title should be at least 5 characters and no more than 200.
        """
        sanitized: str = self.node_title.strip()
        return 5 <= len(sanitized) <= 200

    def is_valid_content(self) -> bool:
        """
        The content should be no more than 10,000 chars long.
        """
        sanitized: str = self.node_content.strip()
        return len(sanitized) <= 10_000

    def add_image(self, newFile=None, newURL=None) -> bool:
        """
        Allows for image to be attached to a Story Node.
        """
        # If both parameters are given, then the image cannot
        # be updated to just one. Return False.
        if newFile is not None and newURL is not None:
            return False
        # newFile is given and can be updated as current image
        elif newFile is not None:
            return self.add_image_from_file(file=newFile)
        # newURL is given and can be updated as current image
        elif newURL is not None:
            return self.add_image_from_url(URL=newURL)
        # Nothing was given. No changes made. Return False
        else:
            return False

    def add_image_from_file(self, file) -> bool:
        """
        Allows for image url to be attached to a Story Node.
        Returns True if attached, otherwise false.
        """
        # Try to find image file
        self.image = file
        try:
            # Update image properties
            self.has_image_file = True
            self.image_url = TextField(default=None)
            self.save()
            return True
        except:
            # Error thrown
            # Change nothing
            return False

    def add_image_from_url(self, URL) -> bool:
        """
        Allows for image url to be linked to a node.
        Returns True if downloaded and attached, otherwise false.
        """
        # Try to find url
        self.image_url = URL
        try:
            # Will not throw error if valid file
            if url(self.image_url):
                # Update image properties
                self.has_image_file = False
                self.image = None
                self.save()
                return True
            # Failsafe for no exception and invalid url
            return False
        except:
            # Error thrown, meaning file does not exist
            # Change nothing
            return False

    def attach_main_tag(self, properties: dict) -> bool:
        '''
        The Node (self) is given a Foreign key to
        its main Tag. The id and properties of the
        Tag are given in a dict:
        {"name_text": Tag.name_text, "countID": Tag.countID, "id": Tag.id}
        Returns True if attached or False otherwise
        '''
        try:
            # Valid Tag attachment
            self.other_tags.add(Tag.objects.get(id=properties["id"]))
            self.main_tag_id = properties["id"]
            self.save()
            return True
        except:
            # Invalid Tag attachment
            return False

    def attach_tag(self, properties: dict) -> bool:
        '''
        The Node (self) is given a relationship to
        many Tags. The id and properties of the
        Tag are given in a dict:
        {"name_text": Tag.name_text, "countID": Tag.countID, "id": Tag.id}
        Returns True if attached or False otherwise
        '''
        try:
            # Attach given Tag to this Node
            self.other_tags.add(Tag.objects.get(id=properties["id"]))
            self.save()
            return True
        except:
            # Invalid Tag attachment
            return False

    def is_mature(self) -> bool:
        """
        Returns True if this node has the "Mature" tag in other_tags.
        """
        return self.other_tags.filter(name_text="Mature").exists()

    def attach_mature_tag(self) -> None:
        """
        Adds the "Mature" tag to this Node.
        If the tag does not already exist, create it. Otherwise, retrieve it
        and add it.
        """
        tag: Tag = None

        # retrieve the mature tag if it exists, otherwise make it
        try:
            tag = Tag.objects.get(name_text="Mature")
        except Tag.DoesNotExist:
            tag = Tag(name_text="Mature")
            tag.save()

        self.other_tags.add(tag)
        self.save()

        return

    def add_reaction(self, emoji: str, user: User) -> bool:
        """
        Adds a reaction to this node.
        """
        if self.is_user_reacted_with_emoji(emoji, user): return False

        reaction: Reaction = Reaction(node=self, emoji=emoji, owner=user)
        reaction.save()
        return True

    def num_reactions_of_emoji(self, emoji: str) -> int:
        """
        Returns a QuerySet of all the reactions to this Node
        with the given emoji.
        """
        return Reaction.objects.filter(node=self, emoji=emoji).count()

    def is_user_reacted_with_emoji(self, emoji: str, user: User) -> bool:
        """
        Returns True if the current user has reacted to this Node.
        """
        return Reaction.objects.filter(node=self, emoji=emoji, owner=user).exists()

    def generate_id(self) -> bool:
        post_id = str(uuid.uuid1())
        checkID = Node.objects.filter(post_id=post_id)
        while (checkID.count() != 0):
            post_id = str(uuid.uuid1())
            checkID = Node.objects.filter(post_id=post_id)
        self.post_id = post_id
        self.save()
        return True


class Report(models.Model):
    # the id of the user who put in the report (set null so we can keep the reports)
    reporting_username = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=False, primary_key=True)

    # the id of the reported posts
    reported_user = models.ForeignKey(User,on_delete=models.CASCADE, default=None,related_name='reported_user')

    # the reason the user was reported (text field)
    report_reason = models.CharField(max_length=600)

    # hold the id for a report
    id_for_report = models.CharField(max_length=100, default="")

    # an id for a report
    post = models.ForeignKey(Node, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return self.id_for_report


class Reaction(Model):
    emoji: CharField = CharField(max_length=1)
    node: ForeignKey = ForeignKey(Node, on_delete=CASCADE, null=True)
    owner: ForeignKey = ForeignKey(User, on_delete=CASCADE, null=True)

