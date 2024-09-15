# NOTE: Тестировать только при рабочем config.
# class TestContest(unittest.TestCase):
#     def testAll(self):
#         ContestInterface().signIn(GlobalConfig().login, GlobalConfig().password)
#         isSkipNext = False

#         homeworksLocalId = ContestInterface().getAvailableHomeworksLocalId()
#         for localId in homeworksLocalId:
#             homework = ContestInterface().getHomework(GlobalConfig().name, localId)
#             id = homework[0]
#             if id == "-1":
#                 continue

#             tasksId = list(range(1, 13))
#             contest = Contest(id, [str(taskId) for taskId in tasksId])
#             for taskLocalId in range(1, len(tasksId) + 1):
#                 contest.selectTask(taskLocalId)
#                 task = contest.currentTask
#                 print(task.name)
#                 print(task.info)
#                 print(task.condition)
#                 print(task.solution)
#                 print(list(task.tests))
#                 if isSkipNext == False:
#                     input_ = input("Skip next ask: yes/no(default): ")
#                     if input_ == "yes" or input_ == "y":
#                         isSkipNext = True

#                 os.system("clear")
