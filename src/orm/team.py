from dash.conf import conf
from marshmallow import Schema, fields, post_load


class TeamExists(Exception):
    """Raised when a team by the specified name already exists."""

    def __init__(self, team):
        self.team = team
        super().__init__()


class TeamSchema(Schema):
    name = fields.Str()
    rounds = fields.Dict(keys=fields.Str, values=fields.Dict(keys=fields.Str, values=fields.Str))

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
        self.rounds = kwargs['rounds'] if 'rounds' in kwargs else {}

        if self.rounds == {}:
            qnumber = 1
            for i in range(1, conf.numberOfRounds + 1):
                round = {}
                for j in range(1, conf.questionsPerRound + 1):
                    round[str(qnumber)] = ""
                    qnumber += 1
                self.rounds[f"Round {i}"] = round

            for i in range(1, conf.numberOfBonusRounds + 1):
                round = {}
                for j in range(1, conf.questionsPerBonusRound + 1):
                    round[str(qnumber)] = ""
                    qnumber += 1
                self.rounds[f"Bonus Round {i}"] = round

    @property
    def total(self):
        total = 0
        for round, questions in self.rounds.items():
            for number, score in questions.items():
                if score != "":
                    total += int(score)
        return total
