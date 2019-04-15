from peewee import *


db = SqliteDatabase('work_log.db')

class WorkLogEntry(Model):
    employee = CharField(max_length = 255)
    date = DateField()
    task_name = CharField(max_length = 255)
    time_spent = IntegerField()
    notes = TextField()
    
    class Meta:
        database = db
   
if __name__ == '__main__':
    db.connect()
    db.create_tables([WorkLogEntry], safe=True)

