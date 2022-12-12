l = [{'domain': {'id': '6', 'name': 'Sports Event'}, 'entity': {'id': '1103026158382141440', 'name': 'Tokyo 2020 Summer Olympics', 'description': 'Tokyo 2020 Summer Olympics '}},
     {'domain': {'id': '10', 'name': 'Person', 'description': 'Named people in the world like Nelson Mandela'}, 'entity': {'id': '733774054713217024', 'name': 'Max Gradel'}},
     {'domain': {'id': '10', 'name': 'Person', 'description': 'Named people in the world like Nelson Mandela'}, 'entity': {'id': '733774784014622720', 'name': 'Eric Bailly'}},
     {'domain': {'id': '60', 'name': 'Athlete', 'description': 'An athlete in the world, like Serena Williams or Lionel Messi'}, 'entity': {'id': '733774054713217024', 'name': 'Max Gradel'}},
     {'domain': {'id': '60', 'name': 'Athlete', 'description': 'An athlete in the world, like Serena Williams or Lionel Messi'}, 'entity': {'id': '733774784014622720', 'name': 'Eric Bailly'}}]
l2 = []
l3 = []
for x in l:
    for y in x.keys():
        if y == 'domain':
            l2.append(x[y])
for x in l2:
    for y in x .keys():
        if y == 'name':
            l3.append(x[y])
for x in l3:
    print(x)