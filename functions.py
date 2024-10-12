from models import Comment
from better_profanity import profanity

def filter_bad_words(text):
    return profanity.censor(text)

def get_coms_count(story):
    comments = Comment.query.filter_by(story_id=story.id).all()
    story.comments = comments  # Update the story object with the comments
    story.comments_count = len(comments)  # Optionally, store the count


def get_pages_count(stories_count):
    if stories_count > 10:
        if stories_count % 10 == 0:
            count = int(stories_count / 10)
        else:
            count = int(stories_count // 10 + 1)
    else:
        count = 1

    return count
