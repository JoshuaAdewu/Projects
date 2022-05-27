from django.db import models

# Create your models here.
class Tag(models.Model):

    name_text = models.CharField(max_length=255) # tag name identifier
    countID = models.IntegerField(default=-1) # unique tag ID
    usage_count = models.IntegerField(default=0) # times used by users
    language = models.CharField(max_length=255) # language used by tag

    # Returns name_text
    def __str__(self):
        return self.name_text

    # Returns True if tag name is valid alphanumeric and
    # greater than 3 characters (valid tag name).
    def is_valid_name(self) -> bool:
        MIN_LEN = 3  # minimum Tag name length
        if str(self.name_text).isalnum() and len(str(self.name_text)) >= MIN_LEN:
            return True
        return False

    # Returns True if tag does not yet exist
    # and can be inserted. False, otherwise.
    def is_new_tag(self) -> bool:
        # If get raises an error, then the Tag does not
        # yet exist. Otherwise, it was found.
        # Warning: get() can raise an error if it found multiple
        # of the same name_text, however, the use of this function
        # should prevent such a case.
        try:
            isOldTag = Tag.objects.get(name_text=self.name_text)
        except:
            # Return True if Tag does not yet exist in db
            return True
        # Return False if Tag already exists in db
        return False

    # Returns True if new tag is saved.
    # False, otherwise.
    def add_new_tag(self) -> bool:
        # If Tag has a valid name and tag, save
        # tag to the database. Return True if
        # added or False if not added.
        if self.is_valid_name() and self.is_new_tag():
            self.countID = Tag.objects.count()
            self.save()
            return True
        return False

    # Returns properties needed to add tag to a node and
    # increments usage count when used.
    def add_tag_to_node(self) -> dict:
        # Increment usage count and save to db
        try:
            existing_tag = Tag.objects.get(name_text=self.name_text)
            existing_tag.usage_count += 1
            existing_tag.save()
        except:
            return {}
        # Return necessary details needed for the
        # connection of a Tag to a node.
        return {"name_text": self.name_text, "countID": self.countID, "id": self.id}

    # Decrements usage count when add fails or user removes
    # their tag. Managed by user of Tag model. Returns new
    # usage count.
    def decrement_usage(self):
        # Check if usage_count is already at zero
        if self.usage_count == 0:
            return self.usage_count
        # Decrement usage_count of Tag
        self.usage_count -= 1
        # Return updated usage_count
        return self.usage_count
