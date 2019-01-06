import csv
import config
import os
from random import randint

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
        self.scores=self.convert_scores(scores)
        self.name=None
        self.mat_no=None

    def get_tlu(self):
        f=lambda x:self.units[x]*self.scores[x]
        return sum(i for i in map(f,range(len(self.units))))

    def convert_scores(self,scores):
        result=[]
        for score in scores:
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
    def process(filenames,title):

        def intify(value):
            try:
                return int(value)
            except ValueError:
                return 0
        def get_name():
            alphabeths="abcdefghijklmnopqrstuvwxyz"
            return "".join([alphabeths[randint(0,25)] for i in range(10)])


        cgpa=open(config.UPLOAD_FOLDER+"/"+title+".csv","w+")
        user={}
        fileobj_reader=[open(name,"r+") for name in filenames]
        namesout=[config.UPLOAD_FOLDER+ "\\out"+title+get_name()+".csv" for name in filenames]
        fileobj_writer=[open(name,"w+") for name in namesout]

        files_reader=[csv.reader(fileobj, delimiter=',', quotechar='|') for fileobj in fileobj_reader]
        files_writer=[csv.writer(fileobj, delimiter=',', quotechar='|') for fileobj in fileobj_writer]

        cgpa_writer=csv.writer(cgpa,delimiter=',', quotechar='|')

        first_line_overall=[]
        error=False
        try:

            for index in range(len(filenames)):
                reader=files_reader[index]
                writer=files_writer[index]

                firstline=[sr for sr in reader.__next__()]
                writer.writerow(firstline)
                end_index_of_scores=firstline.index("TLU")

                if not first_line_overall:
                    first_line_overall.extend(firstline[:end_index_of_scores])
                else:
                    first_line_overall.extend(firstline[3:end_index_of_scores])

                units=[int(sc.split(" ")[2]) for sc in firstline[3:end_index_of_scores]]#hoping this would contain units

                for user_scores in reader:

                    scores=[intify(score) for score in  user_scores[3:end_index_of_scores]]

                    user_gpa=gpa(scores,units)
                    user_gpa.name=user_scores[1]
                    user_gpa.mat_no=user_scores[2]
                    if user_scores[1] not in user:
                        user[user_scores[1]]=[user_gpa]
                    else:
                        user[user_scores[1]].append(user_gpa)

            cgpa_writer.writerow(first_line_overall+["TLU","CGPA"])
            outjson={}
            outjson["header"]=first_line_overall+["TLU","CGPA"]
            outjson["users"]=[]
            index=1
            for user_gpa in user:
                user_gpas=user[user_gpa]
                if not user_gpas:
                    index+=1
                    continue
                cgpa_user=CGPA(gpas=user_gpas)
                cgpa_user.name,cgpa_user.mat_no=user_gpas[0].name,user_gpas[0].mat_no
                cgpa_writer.writerow([index,cgpa_user.name,cgpa_user.mat_no]+\
                            cgpa_user.main_score+\
                            [cgpa_user.get_tlu(),cgpa_user.get_cgpa()])
                outjson["users"].append(cgpa_user.to_dict())
                index+=1
        except Exception:
            error=True
        #we need to close the file to trigger a flush
        for file_a,file_b in zip(fileobj_reader,fileobj_writer):
            file_a.close()
            file_b.close()

        [os.remove(name) for name in namesout] #cleaning up

        outjson["error"]=False
        outjson["success_msg"]="Successfully Complied"
        cgpa.close()
        outjson["nameoffile"]=title+".csv"

        return outjson
class CGPA:
    def __init__(self,gpas=[]):
        self.gpas=gpas
        self.units=[]
        self.scores=[]
        self.main_score=[]
        for gp in gpas:
            self.units.extend(gp.units)
            self.scores.extend(gp.scores)
            self.main_score.extend(gp.main_score)
        self.gp=gpa(self.main_score,self.units)
        self.name=None
        self.mat_no=None

    def add_gpa(self,gpa):
        self.gpas.extend(gpa)
        self.units.extend(gpa.units)
        self.scores.extend(gpa.scores)
        self.main_score.extend(gp.main_score)
        self.gp=gpa(self.main_score,self.units)


    def get_tlu(self):
        return self.gp.get_tlu()

    def get_cgpa(self):
        return self.gp.get_gpa()

    def to_dict(self):
        obj={}
        obj["scores"]=self.scores
        obj["mainscore"]=self.main_score
        obj["name"]=self.name
        obj["matno"]=self.mat_no
        obj["cgpa"]=self.get_cgpa()
        obj["tlu"]=self.get_tlu()

        return obj

if __name__=="__main__":
    a="C:\\Python35\\upshot-master\\upshot-master\\upshot\\SEMESTER1.csv"
    b="C:\\Python35\\upshot-master\\upshot-master\\upshot\\SEMESTER2.csv"
    print(gpa.process([a,b],"test"))