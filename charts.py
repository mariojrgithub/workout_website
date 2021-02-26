import numpy as np

# final function to obtain x and y values and labels
def create_axis(cardio, resistance, month):

  # define exercises
  exercises = ['Bike', 'Spin', 'Swim', 'Rowing', 'Walk', 'Run', 'Hike', 
          'Stairs', 'Press', 'Pushup', 'Tricep Ext', 'Pull/Row', 'Pullup', 
          'Pulldown', 'Bicep Curl', 'Squat', 'Stepup', 'Lunge', 'Bridge', 
          'Hamstring Curl', 'Plank', 'Crunches', 'Side Plank', 'Ab Rotation']

  # get two objects, cardio and resistance, month specific
  cardio_list = []
  resistance_list = []

  for i in cardio:
    if int(i.date.split('-')[1]) == month:
      cardio_list.append([i.name, i.date])

  for i in resistance:
    if int(i.date.split('-')[1]) == month:
      resistance_list.append([i.name, i.date])

  # combined cardio and resistance list
  ex_list = cardio_list + resistance_list

  # extract dates and names
  dates = [x[1] for x in ex_list]
  names = [x[0] for x in ex_list]

  # extract days
  days = [x.split('-')[2] for x in dates]

  user = []
  for i in names:
    for k, v in enumerate(exercises):
      if i == v:
        user.append([k, i])

  user = list(zip(user, days))  

  # determine x_axis
  if month in [1, 3, 5, 7, 8, 10, 12]:
    x_axis = ['0' + str(x) if len(str(x)) == 1 else str(x) for x in range(1, 32)]
  elif month == 2:
    x_axis = ['0' + str(x) if len(str(x)) == 1 else str(x) for x in range(1, 29)]
  else:
    x_axis = ['0' + str(x) if len(str(x)) == 1 else str(x) for x in range(1, 31)]

  # get y_axis information
  y_axis = []
  for i in x_axis:

    for x in user:
      if i == x[1]:
        y_axis.append([x[1], x[0]])
    if i not in days:
      y_axis.append([i, 0])  

  # isolate x values
  x = [int(x[0]) for x in y_axis]

  # isolate y values
  y = []
  # isolate y labels
  y_labels = []
  for i in y_axis:
    if type(i[1]) == list:
      y.append(i[1][0] + 1)
      y_labels.append(i[1][1])
    else:
      y.append(i[1]) 

  # pie chart data
  cardio_count = len(set([x.date for x in cardio])) 
  resistance_count = len(set([x.date for x in resistance]))

  cardio_percent = int((cardio_count / cardio_count + resistance_count) * 10)
  resistance_percent = int((resistance_count / cardio_count + resistance_count) * 10)

  return x, y, exercises, cardio_percent, resistance_percent