import csv

class gpa:
    def __init__(self,scores,units,user=None):
        """ scores is a list conataining user scores for each course
            units id the unit of each course
         """
    
        if len(scores)!=len(units):
            raise ValueError("invalid paramters")
        self.user=user
        self.units=units
        self.main_score=scores
        self.scores=self.covert_scores(scores)

    def get_tlu(self):
        f=lambda x:self.units[x]*self.scores[x]
        return sum(i for i in map(f,range(len(self.units))))

    def convert_scores(self,scores):
        result=[]
        for score in result:
            if score>=70:
                result.append(5)
            elif 60<= score<70:
                result.append(4)
            elif 50<=score<60:
                result.append(3)
            elif 45<=score<50:
                result.append(2)
            else:
                result.append(0)
        return result

    def get_unit_sum(self):
        return sum(self.units)

    def get_gpa(self):
        return self.get_tlu()/self.get_unit_sum()
    
    @staticmethod
    def process(filename):
        result=[]
        with open(filename, newline='') as csvfile:
            with open("out"+filename,"wb+") as csvfileout:
                reader = csv.reader(csvfile, delimiter=',', quotechar='|')
                writer=csv.writer(csvfile, delimiter=',', quotechar='|')
                units=[int(sc) for sc in reader.__next__()]#hoping this would contain units
                for user_scores in reader:
                    scores=user_scores[:]#would probably br within some particular range
                    user_gpa=gpa(scores,units)
                    current_user={}
                    current_user["gpa"]=user_gpa.get_gpa()
                    current_user["tlu"]=user_gpa.get_tlu()
                    current_user["scores"]=scores
                    current_user["units"]=units
                    current_user["matno"]="matno"
                    result.append(current_user)
            return result


        
    