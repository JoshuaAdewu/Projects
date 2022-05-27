from django.test import TestCase  # Django testing functionality
from managetags.models import Tag  # Test Tag model

class TagModelTests(TestCase):

    # Returns False for tags created with incorrect
    # names when given a name.
    # Functions to test: is_valid_name
    def test_was_tag_name_valid(self):
        # Names must be greater than 2 chars
        short: Tag = Tag(name_text="ab")
        is_name_correct = short.is_valid_name()
        self.assertIs(is_name_correct, False)
        # Names must not contain non-alphanumeric chars
        end_space: Tag = Tag(name_text="name ")
        is_name_correct = end_space.is_valid_name()
        self.assertIs(is_name_correct, False)
        # Names must not contain non-alphanumeric chars
        middle_space: Tag = Tag(name_text="name name")
        is_name_correct = middle_space.is_valid_name()
        self.assertIs(is_name_correct, False)
        # Names must not contain non-alphanumeric chars
        non_alpha_num: Tag = Tag(name_text="nameAB(")
        is_name_correct = non_alpha_num.is_valid_name()
        self.assertIs(is_name_correct, False)
        # Names must be alphanumeric with at least 3 chars
        alpha_num: Tag = Tag(name_text="ab1")
        is_name_correct = alpha_num.is_valid_name()
        self.assertIs(is_name_correct, True)

    # Returns False for tags that don't exist in the db
    # after insertion.
    # Functions to test: add_new_tag, add_tag_to_node
    def test_was_tag_added(self):
        original_count = Tag.objects.count() # original count of Tags

        # INSERT NEW VALID TAG Note: Adding a tag checks for these conditions,
        # but Tag model user must manage user input or Tag is rejected.
        TagToInsert = Tag(name_text="name123", language="en_US")
        # Step 1: Check for valid name
        self.assertIs(TagToInsert.is_valid_name(), True)
        # Step 2: Check if it exists
        self.assertIs(TagToInsert.is_new_tag(), True)
        # Step 3: Save Tag
        self.assertIs(TagToInsert.add_new_tag(), True)

        # Check if new count is correct
        new_count = Tag.objects.count()  # new count of Tags after insertion
        tag_in_db = (new_count == original_count + 1)
        self.assertIs(tag_in_db, True)

    # Returns False for tags created with incorrect
    # ID when given an ID.
    # Functions to test: add_new_tag
    def test_was_tag_ID_valid(self):
        # INSERT NEW VALID TAG Note: Adding a tag checks for these conditions,
        # but Tag model user must manage user input or Tag is rejected.
        TagToInsert = Tag(name_text="name12", language="en_US")
        # Step 1: Check for valid name
        self.assertIs(TagToInsert.is_valid_name(), True)
        # Step 2: Check if it exists
        self.assertIs(TagToInsert.is_new_tag(), True)
        # Step 3: Save Tag
        self.assertIs(TagToInsert.add_new_tag(), True)

        # Check if new Tag's ID is correct
        new_count = Tag.objects.count()  # new count of Tags after insertion
        tag_ID = (new_count == TagToInsert.countID + 1)
        self.assertIs(tag_ID, True)

    # Returns False when an invalid tag is
    # inserted.
    # Functions to test: add_new_tag, add_tag_to_node, decrement_usage
    def test_was_bad_tag_rejected(self):
        # INSERT NEW VALID TAG Note: Adding a tag checks for these conditions,
        # but Tag model user must manage user input or Tag is rejected.
        TagToInsert = Tag(name_text="name 123", language="en_US")
        # Check if tag with invalid name is rejected
        self.assertIs(TagToInsert.add_new_tag(), False)

        # Check if tag added to node can be decremented after
        # "rejection" where tag is desired to be removed.
        TagToInsert = Tag(name_text="node", language="en_US")
        TagToInsert.add_new_tag()
        TagToInsert.add_tag_to_node()
        self.assertIs((TagToInsert.decrement_usage() == 0), True)

        # Check if tag returns valid dictionary with
        # identifying properties.
        TagToInsert = Tag(name_text="valid", language="en_US")
        TagToInsert.add_new_tag()
        insertDict = TagToInsert.add_tag_to_node()
        self.assertIs((insertDict["name_text"] == "valid"
                       and insertDict["countID"] == Tag.objects.count() - 1
                       and insertDict["id"] == TagToInsert.id), True)

    # Returns False for tags that don't reject
    # insertion when repeated.
    # Functions to test: add_new_tag
    def test_was_tag_added_without_repeat(self):
        # Check if tag that exists is rejected
        TagToInsert = Tag(name_text="name1", language="en_US")
        TagToInsert.add_new_tag()
        self.assertIs(TagToInsert.add_new_tag(), False)

    # Tests the user input form for creating
    # new tags.
    def test_tag_creation_by_user_input(self):
        name = "valid"
        response = self.client.post("/story/addtags/create/", data={'tag_name': name})
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Tag.objects.get(name_text=name))
