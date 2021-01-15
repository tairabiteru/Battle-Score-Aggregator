from marshmallow import Schema, fields, post_load


class TeamExists(Exception):
    """Raised when a team by the specified name already exists."""

    def __init__(self, team):
        self.team = team
        super().__init__()


class TeamSchema(Schema):
    name = fields.Str()
    questions = fields.Dict(keys=fields.Str, values=fields.Str)

    @post_load
    def make_obj(self, data, **kwargs):
        return Team(**data)


class Team:
    """
    Define a team.

    Stores the team name, and the questions as a dict.
    Each question has a number associated with it, which when
    all are totaled, results in the score.
    """
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.questions = kwargs['questions'] if 'questions' in kwargs else {}

        if self.questions == {}:
            for i in range(1, 64):
                self.questions[str(i)] = ""

    @property
    def total(self):
        total = 0
        for number, score in self.questions.items():
            if score != "":
                total += int(score)
        return total
