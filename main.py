import sys


class Task:
    def __init__(self, fajlSora: str) -> None:
        adatok = fajlSora.split(",")
        self.id: str = adatok[0]
        self.prior = adatok[1] == "1" if True else False
        self.arrive = int(adatok[2])
        self.time = int(adatok[3])
        self.wait = 1
        self.voltmar = True
        self.dirty = False

    def __str__(self) -> str:
        return f"{self.id}, {self.time}, {self.voltmar}"


class Order:
    def __init__(self) -> None:
        self.order = ""

    def __str__(self) -> str:
        return self.order

    def add(self, id: str) -> None:
        if self.order == "":
            self.order += id
        elif self.order[len(self.order)-1] != id:
            self.order += id


def addToList(tik: int) -> None:
    db = sum(map(lambda task: task.arrive == tik, tasks))
    for i in range(db):
        for task in tasks:
            if task.arrive == tik:
                if task.prior:
                    siker = False
                    for i in reversed(range(len(highPriorTasks))):
                        if highPriorTasks[i].voltmar and highPriorTasks[i].arrive != task.arrive:
                            highPriorTasks.insert(i, task)
                            siker = True
                            break
                    if not siker: highPriorTasks.append(task)
                else:
                    lowPriorTasks.append(task)
                tasks.remove(task)
                break


def resetWait() -> None:
    tasks.sort(key=lambda task: task.arrive)
    for task in tasks:
        if wait.get(task.id) == None:
            wait[task.id] = 0


tasks: list[Task] = []
for line in sys.stdin:
    if len(line.split(",")) == 4:
        tasks.append(Task(line.strip()))


order = Order()
wait: dict[str, int] = {}
lowPriorTasks: list[Task] = []
highPriorTasks: list[Task] = []
resetWait()
addToList(0)


tik: int = 1

while len(highPriorTasks) != 0 or len(lowPriorTasks) != 0 or len(tasks) != 0:
    # Ha van high prior akkor azt
    if len(highPriorTasks) != 0:
        task = highPriorTasks[0]
        task.time -= 1
        task.wait -= 1
        order.add(task.id)
        print(f"{tik} - {task.id}-H ({task.time+1}->{task.time})")
        task.voltmar = not task.voltmar

        if task.time == 0:
            wait[task.id] = task.wait
            highPriorTasks.remove(task)
        elif task.voltmar:
            highPriorTasks.remove(task)
            highPriorTasks.append(task)

    # Ha nincs akkor low prior-t
    elif len(lowPriorTasks) != 0:
        curTask = lowPriorTasks[0]
        for task in lowPriorTasks:
            if task.time < curTask.time:
                curTask = task
        curTask.time -= 1
        curTask.wait -= 1
        order.add(curTask.id)
        print(f"{tik} - {curTask.id}-L ({curTask.time+1}->{curTask.time})")
        lowPriorTasks.remove(curTask)
        wait[curTask.id] = curTask.wait
        if curTask.time != 0:
            lowPriorTasks.insert(0, curTask)

    # Lehet h most egyikbe sincs, de még van ami nem jött meg az ütemezőbe
    for task in lowPriorTasks:
        task.wait += 1
    for task in highPriorTasks:
        task.wait += 1
    # Ha van várakozó akkor azt számolni
    #   Amit csinálok azt csökkenteni, amúgy az összes bentlévőt növelni
    addToList(tik)
    tik += 1


print(order)
db = len(wait)
i = 0
for item in wait:
    i += 1
    if i == db:
        print(f"{item}:{wait[item]}", end="")
    else:
        print(f"{item}:{wait[item]}", end=",")
