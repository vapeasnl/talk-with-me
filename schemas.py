from marshmallow import Schema, fields

class UserSchema(Schema):
    username = fields.Str()
    profile_picture_url = fields.Str()

class CommentSchema(Schema):
    id = fields.Int()
    text = fields.Str()
    likes = fields.Int()
    dislikes = fields.Int()
    user = fields.Nested(UserSchema)

class StorySchema(Schema):
    id = fields.Int()
    title = fields.Str()
    text = fields.Str()
    likes = fields.Int()
    dislikes = fields.Int()
    user_id = fields.Int()
    author = fields.Nested(UserSchema)
    comments = fields.Nested(CommentSchema, many=True)
