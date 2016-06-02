from Queue import Queue
import abc

def coroutine():
    pass

class SysCall():
    __metaclass__=abc.ABCMeta
    @abc.abstractmethod
    def handle(self):
        pass

class GetTid(SysCall):
    def handle(self):
        self.task.sendVal=self.task.tid
        self.sche.onSchedule(self.task)

class NewTask(SysCall):
    def __init__(self,iterTask):
        self.iterTask=iterTask
    def handle(self):
        tid=self.sche.new(iterTask)
        self.task.sendVal=tid
        self.sche.onSchedule(self.task)

class KillTask(SysCall):
    def __init__(self,tid):
        self.tid=tid
    def handle(self):
        task=self.sche.dirActTask[tid]
        if task:
            task.close()
            self.task.sendVal=True
        else:
            self.task.sendVal=False
        self.sche.onSchedule(self.task)

class Waitting(SysCall):
    def __init__(self,tid):
        self.tid=tid
    def handle(self):
        returnVal=self.sche.waitting(self.task,tid)
        self.task.sendVal=returnVal
        if not returnVal:
            self.sche.onSchedule(self.task)


class Task():
    Tid=0
    def __init__(self,iterTask):
        Task.Tid+=1
        self.tid=Task.Tid
        self.iterTarget=iterTask
        self.sendVal=None

    def run(self):
        return self.funtarget.send(self.sendVal)

class scheduler():
    def __init__(self):
        self.queReadyTask=Queue()
        self.dirActTask={}
        self.dirWaitting={}

    def new(self,iterTask):
        task=Task(iterTask)
        self.onSchedule(task)
        self.dirActTask[task.tid]=task
        return task.tid

    def exit(self,task):
        print("task %d terminated",task.tid)
        del difActTask[task.tid]
        #all waitting task will free
        for t in self.dirWaitting[task.tid]
            self.onSchedule(t)

    def onSchedule(self,task):
        self.queReadyTask.put(task)

    def waitting(self,task,tid):
        if tid in self.dirActTask:
            self.dirWaitting.setdefault(tid,[]).append(task)
            return True
        else
            return False

    def boot(self):
        task=self.queReadyTask.get()
        while True:
            try:
                returnVal=task.run()
                if isinstance(returnVal,SysCall):
                    returnVal.task=task
                    returnVal.sche=self
                    returnVal.handle()
                    continue
            except StopIteration:
                self.exit(task)
                continue
            self.queReadyTask.put(task)

