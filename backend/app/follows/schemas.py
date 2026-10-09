from pydantic import BaseModel, ConfigDict


class FollowOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    follower_id: int
    followee_id: int
