from django.test import TestCase
from tellmeastory.models import User, Report, Ban, Node, Reaction
from managetags.models import Tag

RND_USERNAME: str = "RandomUser"
HEART: str = "💙"
SMILE: str = "🙂"
IMP: str = "😈"

def insert_story_node(post_id: str, node_title: str, node_content: str, node_author: User) -> Node:
    return Node.objects.create(
        post_id=post_id,
        node_title=node_title,
        node_content=node_content,
        node_author=node_author

    )

class UserModelTests(TestCase):


    def test_valid_username(self) -> None:
        """
        is_valid_username() should return False if the desired
        username contains anything other than Unicode word chars,
        numbers, spaces, hyphens, or underscores.
        Similarly, the username should have a length of 5 <= name <= 14.
        """
        invalid_name_bang: str = "Woah!"
        invalid_name_short: str = "hey"
        invalid_name_long: str = "0123456789TenEleven"
        valid_name: str = "GodHimself"

        bang: User = User(username=invalid_name_bang)
        short: User = User(username=invalid_name_short)
        long: User = User(username=invalid_name_long)
        valid: User = User(username=valid_name)

        self.assertIs(bang.is_valid_username(), False)
        self.assertIs(short.is_valid_username(), False)
        self.assertIs(long.is_valid_username(), False)
        self.assertIs(valid.is_valid_username(), True)

        return

    def test_unique_username_checking(self) -> None:
        """
        is_unique_username() should return False if the desired
        username is not registered to another user account.
        """
        desired_dup_name: str = "Cringe"
        desired_uniq_name: str = "NotCringe"

        orig_user: User = User(username=desired_dup_name)
        orig_user.save()
        dup_user: User = User(username=desired_dup_name)
        new_orig_user: User = User(username=desired_uniq_name)

        self.assertIs(dup_user.is_unique_username(), False)
        self.assertIs(new_orig_user.is_unique_username(), True)

        return

    def test_valid_display_name(self) -> None:
        """
        is_valid_display_name() should return False if the desired
        display name does not have a length of 5 <= name <= 20.
        """
        invalid_too_short: str = ":)"
        invalid_too_long: str = "Not smile because that would be too short"
        valid: str = "God Himself"

        short: User = User(display_name=invalid_too_short)
        long: User = User(display_name=invalid_too_long)
        good: User = User(display_name=valid)

        self.assertIs(short.is_valid_display_name(), False)
        self.assertIs(long.is_valid_display_name(), False)
        self.assertIs(good.is_valid_display_name(), True)

        return
      
    def test_can_view_mature(self) -> None:
        """
        is_mature() should return True if the user has marked
        their account as mature.
        """
        user: User = User(mature=True)
        self.assertTrue(user.is_mature())

        return


def insert_node_w_author(author: User, title: str, content: str) -> Node:
    return Node.objects.create(
        node_author=author,
        node_title=title,
        node_content=content
    )

class testDatabaseRetrieval(TestCase):
    #testing Post database functionality
    def test_get_retrieval_node(self):

        # create objects
        user1 = User.objects.create(username="user1", password="test", display_name = "Warrior", admin = False )
        user2 = User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)


        # create some objects
        insert_story_node(post_id="4ad56262a25", node_title="My first post!", node_content="First Story", node_author=user1)
        insert_story_node(post_id="26q2aa263a2", node_title="My second post!", node_content="Second Story", node_author=user2)


        # get by the post_id (primary key)
        first_post = Node.objects.get(post_id="4ad56262a25")
        second_post = Node.objects.get(post_id="26q2aa263a2")

        #check if the text is equal in the database
        self.assertEqual(first_post.node_title, "My first post!")
        self.assertEqual(second_post.node_title, "My second post!")

        return

    #testing UserTable database functionality
    def test_get_retrieval_user(self):

        # create objects
        User.objects.create(username="user1", password="test", display_name="Warrior", admin=False)
        User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)


        #get by the user_id (primary key)
        first_user = User.objects.get(username="user1")
        second_user = User.objects.get(username="user2")

        #check if the passwords are equal
        self.assertEqual(first_user.password, "test")
        self.assertEqual(second_user.password, "test")

        return

class testReporting(TestCase):
    def test_report(self):

        #create objects
        user1 = User.objects.create(username="user1", password="test", display_name="Warrior", admin=False)
        user2 = User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)

        # create some objects
        newNode = insert_story_node(post_id="4ad56262a25", node_title="My first post!", node_content="First Story", node_author=user2)

        Report.objects.create(reporting_username=user1,reported_user=user2,report_reason="Racism",id_for_report="6a92agh0aw",post=newNode)

        getReports = Report.objects.filter(reporting_username=user1)
        reportCount = getReports.count()
        self.assertEqual(reportCount, 1)

        return

    def test_ban(self):

        # create some objects
        user = User.objects.create(username="user2", password="test", display_name="Gunner", admin=False)

        insert_story_node(post_id="4ad56262a25", node_title="My first post!", node_content="First Story", node_author=user)

        #simulate a ban
        Ban.objects.create(bannedUser=str(user))

        User.delete(User.objects.get(username=str(user)))

        #check if the current user is in the User table and Ban table
        get_user = User.objects.filter(username=str(user))
        get_banned_user = Ban.objects.filter(bannedUser=str(user))


        self.assertEqual(get_user.exists(),False)
        self.assertNotEqual(get_banned_user, None)

        return


class NodeModelTests(TestCase):
    def setUp(self):
        User.objects.create(
            username=RND_USERNAME,
            password="password",
            display_name="Random User"
        )
        return

    def test_foreign_key_relationship(self) -> None:
        """
        The Node class should have a ForeignKey relationship to the
        User class.
        i.e. A User should have many Nodes, but a Node should have one User.
        """
        user: User = None
        try: user = User.objects.get(username=RND_USERNAME)
        except: pass

        self.assertNotEqual(user, None)

        # insert three nodes into the database
        # all of these nodes should have the same author
        node1: Node = insert_node_w_author(user, "Node 1", "Content 1")
        node2: Node = insert_node_w_author(user, "Node 2", "Content 2")
        node3: Node = insert_node_w_author(user, "Node 3", "Content 3")

        for node in [node1, node2, node3]:
            self.assertEqual(node.node_author, user)

        # check to see if the user has the correct number of nodes

        return

    def test_node_updates_when_user_does(self) -> None:
        """
        When a user updates their User account, the node's key to the
        user should be updated as well.
        """
        user: User = None
        try: user = User.objects.get(username=RND_USERNAME)
        except: pass

        self.assertNotEqual(user, None)

        # insert a node into the database
        node: Node = insert_node_w_author(user, "NodeTitle", "Content")

        user.display_name = "New Display Name"
        user.save()

        self.assertEqual(node.node_author.display_name, user.display_name)

        return

    def test_is_valid_title(self) -> None:
        """
        is_valid_title() should return False if the desired title
        does not have a length of 5 <= node_title <= 200.
        """
        short_title: str = "Yo!"
        long_title: str = "Hi :)" * 1000
        whitespace_short: str = "                Yo!        "
        whitespace_long: str = f"{' ' * 100} {'Hi :)' * 1000} {' ' * 100}"
        valid: str = "Today I did a thing and blah blah blah"

        short: Node = Node(node_title=short_title)
        long: Node = Node(node_title=long_title)
        w_short: Node = Node(node_title=whitespace_short)
        w_long: Node = Node(node_title=whitespace_long)
        good: Node = Node(node_title=valid)

        self.assertIs(short.is_valid_title(), False)
        self.assertIs(long.is_valid_title(), False)
        self.assertIs(w_short.is_valid_title(), False)
        self.assertIs(w_long.is_valid_title(), False)
        self.assertIs(good.is_valid_title(), True)

        return

    def test_is_valid_content(self) -> None:
        """
        is_valid_content() should return False if the desired title
        does not have a length of node_title <= 10_000.
        """
        long_content: str = "Hi :)" * 10000
        whitespace_long: str = f"{' ' * 100} {'Hi :)' * 10000} {' ' * 100}"
        valid: str = "WE WENT TO WALMART AND WE GOT SOME..... **corn flakes**"

        long: Node = Node(node_content=long_content)
        w_long: Node = Node(node_content=whitespace_long)
        good: Node = Node(node_content=valid)

        self.assertIs(long.is_valid_content(), False)
        self.assertIs(w_long.is_valid_content(), False)
        self.assertIs(good.is_valid_content(), True)

        return

    def test_is_mature(self) -> None:
        """
        is_mature() should return True if the node has a mature tag.
        """
        new_node: Node = Node(node_title="BIG TITLE!!!")
        new_node.save()
        self.assertFalse(new_node.is_mature())
        
        tag: Tag = Tag(name_text="Mature", language="en")
        self.assertTrue(tag.add_new_tag())
        self.assertTrue(new_node.attach_tag(tag.add_tag_to_node()))

        self.assertTrue(new_node.is_mature())

        return

    def test_add_reaction(self) -> None:
        """
        add_reaction() should add a Reaction to a Node and return True.
        Attempting to add the same Reaction with the same User should return False.
        Also tests is_user_reacted_with_emoji().
        """
        user: User = None
        try: user = User.objects.get(username=RND_USERNAME)
        except: pass

        self.assertNotEqual(user, None)

        node: Node = insert_node_w_author(user, "NodeTitle", "Content")
        node.save()

        self.assertTrue(node.add_reaction(IMP, user))
        self.assertFalse(node.add_reaction(IMP, user))

        return

    def test_num_reactions_of_emoji(self) -> None:
        """
        num_reactions_of_emoji should be used to determine what number
        to display on a Node's view.
        """
        user: User = None
        try: user = User.objects.get(username=RND_USERNAME)
        except: pass

        self.assertNotEqual(user, None)

        node: Node = insert_node_w_author(user, "NodeTitle", "Content")
        node.save()

        self.assertEqual(node.num_reactions_of_emoji(IMP), 0)
        self.assertEqual(node.num_reactions_of_emoji(HEART), 0)

        node.add_reaction(IMP, user)
        node.add_reaction(HEART, user)

        self.assertEqual(node.num_reactions_of_emoji(IMP), 1)
        self.assertEqual(node.num_reactions_of_emoji(HEART), 1)

        return

class ReactionModelTests(TestCase):
    def setUp(self):
        User.objects.create(
            username=RND_USERNAME,
            password="password",
            display_name="Random User"
        )
        return

    def test_foreign_key_relationship_w_user(self) -> None:
        """
        The Reaction class should have a ForeignKey relationship to the
        User class.
        i.e. A User should have many Reactions, but a Reaction should have one
        User.
        """
        user: User = None
        try: user = User.objects.get(username=RND_USERNAME)
        except: pass

        self.assertNotEqual(user, None)

        # insert three reactions into the database
        # all of these reactions should have the same author
        reaction1: Reaction = Reaction(owner=user, emoji=HEART)
        reaction2: Reaction = Reaction(owner=user, emoji=SMILE)
        reaction3: Reaction = Reaction(owner=user, emoji=IMP)

        for reaction in [reaction1, reaction2, reaction3]:
            reaction.save()
            self.assertEqual(reaction.owner, user)

        return

    def test_foreign_key_relationship_w_author(self) -> None:
        """
        The Reaction class should have a ForeignKey relationship to the
        Node class.
        i.e. A Node should have many Reactions, but a Reaction should have one
        Node.
        """
        new_node: Node = Node(node_title="BIG TITLE!!!")
        new_node.save()

        # insert three reactions into the database
        # all of these reactions should have the same node
        reaction1: Reaction = Reaction(node=new_node, emoji=HEART)
        reaction2: Reaction = Reaction(node=new_node, emoji=SMILE)
        reaction3: Reaction = Reaction(node=new_node, emoji=IMP)

        for reaction in [reaction1, reaction2, reaction3]:
            reaction.save()
            self.assertEqual(reaction.node, new_node)

        return
