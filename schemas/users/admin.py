from base import UserBaseSchema


class AdminSchema(UserBaseSchema):
    class AdminSchema(UserBaseSchema):
        permissions: list[str] = []   # ["ban_users", "delete_content", "view_stats"]
