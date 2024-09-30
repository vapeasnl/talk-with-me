from models import Comment


def get_coms_count(story):
    # Utilisez story_id pour filtrer les commentaires
    coms_count = Comment.query.filter_by(story_id=story.id).count()
    return coms_count  # Retourner le nombre de commentaires

def get_pages_count(stories_count):
    if stories_count > 10:
        if stories_count % 10 == 0:
            count = int(stories_count / 10)
        else:
            count = int(stories_count // 10 + 1)
    else:
        count = 1

    return count
