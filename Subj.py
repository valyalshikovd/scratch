class Subj:

    def __init__(self,
                 year='',
                 semester='',
                 curse='',
                 subject='',
                 reporting='',
                 lecturer='',
                 first_att='',
                 second_att='',
                 third_att='',
                 weighted_score='',
                 additional_score='',
                 exam_score='',
                 exam=''):
        self.year = year
        self.semester = semester,
        self.curse = curse,
        self.subject = subject[0:15] + "...",
        self.reporting = reporting,
        self.lecturer = lecturer,
        self.first_att = first_att,
        self.second_att = second_att,
        self.third_att = third_att,
        self.weighted_score = weighted_score,
        self.additional_score = additional_score,
        self.exam_score = exam_score,
        self.exam = exam

    def to_string(self):
        s = "Семестр " + self.semester[0] + " | " + self.subject[0]+ " | " + self.first_att[
            0] + " | " + self.second_att[0] + " | " + self.third_att[0] + " | " + self.exam_score[0]
        return s
