import csv
import jsonlines

entity = {1: '分类', 2: '名称', 3: '补充', 4: '症状', 5: '步骤'}
entity_1 = open('data/entity_1.csv', 'w', encoding='UTF-8', newline='')
entity_2 = open('data/entity_2.csv', 'w', encoding='UTF-8', newline='')
entity_3 = open('data/entity_3.csv', 'w', encoding='UTF-8', newline='')
entity_4 = open('data/entity_4.csv', 'w', encoding='UTF-8', newline='')
entity_5 = open('data/entity_5.csv', 'w', encoding='UTF-8', newline='')
relations = open('data/relation.csv', 'w', encoding='UTF-8', newline='')
e1 = csv.writer(entity_1)
e2 = csv.writer(entity_2)
e3 = csv.writer(entity_3)
e4 = csv.writer(entity_4)
e5 = csv.writer(entity_5)
re = csv.writer(relations)
e1.writerow([entity[1]])
e2.writerow([entity[2], entity[1]])
e3.writerow([entity[3]])
e4.writerow([entity[4]])
e5.writerow([entity[5]])
re.writerow(['from', 'to', 'relation'])

with jsonlines.open('data/root.jsonl') as fp:
    for line in fp:
        Map = {}
        entityMap = {}
        Id = line['id']
        Text = line['text']
        Entities = line['entities']
        Relations = line['relations']
        text1 = ''
        for index, value in enumerate(Text):
            Map[index] = value
        for values in Entities:
            if values['label'] == entity[1]:
                for index in range(values['start_offset'], values['end_offset']):
                    text1 += Map[index]
        for values in Entities:
            text = ''
            for index in range(values['start_offset'], values['end_offset']):
                text += Map[index]
            entityMap[values['id']] = text
            if values['label'] == entity[2]:
                e2.writerow([text, text1])
            elif values['label'] == entity[3]:
                e3.writerow([text])
            elif values['label'] == entity[4]:
                e4.writerow([text])
            elif values['label'] == entity[5]:
                e5.writerow([text])
        for values in Relations:
            re.writerow([entityMap[values['from_id']], entityMap[values['to_id']], values['type']])

fp.close()
