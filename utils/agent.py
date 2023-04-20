import os.path

from py2neo import *
import re
from utils import nlp


def run(question):
    g = Graph('http://neo4j:root@localhost:7474/')
    answer = ''
    file_path = os.path.dirname(__file__)
    # 定义查询分类词典
    # 1:查找别名,2:查找主名,3:查找药的性状、气味,4:查找药的功效(主治),5:查找生什么病用什么药,6:查找某病怎么治
    name = ['别名', '别号', '又名', '小名', '昵称']
    appearance = ['气味', '性状', '气息']
    effect = ['作用', '效用', '主治', '功效', '效力', '功用', '效果']
    query = nlp.run(question)
    subject = ['是', '介绍', '说明', '解释']

    def check_verb(self):
        with open(file_path + "/data/action.txt", "r", encoding='UTF-8') as file:
            action = file.readlines()
            action = [x.strip() for x in action]
            file.close()
        for el in action:
            temp = re.match(self, el)
            if temp:
                return True
        return False

    def check_object(self):
        with open(file_path + "/data/object.txt", "r", encoding='UTF-8') as file:
            action = file.readlines()
            action = [x.strip() for x in action]
            file.close()
        for el in action:
            temp = re.search(el, self)
            if temp:
                return True
        return False

    def query_med(self):
        _name = query_medicine_by_name(g, self)
        answer = []
        if _name:
            for value in _name:
                value = dict(value['n'])
                result = query_add_by_name_and_category(g, value['name'], value['category'])
                if result:
                    answer.append({'category': value['category'], 'name': value['name'],
                                   'appearance': dict(result[0]['n'])['name']})
                else:
                    is_true = False
                    _value = query_name_by_nickname_and_category(g, value['name'], value['category'])
                    for _el in _value:
                        _temp = dict(_el['n'])
                        if value['category'] == _temp['category']:
                            _value = _temp
                            is_true = True
                            break
                    if is_true:
                        _appearance = query_add_by_name_and_category(g, _value['name'], _value['category'])
                        if _appearance:
                            _appearance = dict(_appearance[0]['n'])['name']
                        else:
                            _appearance = ''
                        answer.append(
                            {'category': _value['category'], 'name': _value['name'], 'appearance': _appearance})
            return answer

    def query_nickname(self):
        answer = ''
        temp = query_med(self)
        for value in temp:
            nickname = query_nickname_by_name_and_category(g, value['name'], value['category'])
            if nickname:
                str1 = '【' + value['category'] + value['name'] + '】释名'
                answer += str1
                for el in nickname:
                    _temp = dict(el['n'])['name']
                    if _temp != self:
                        answer += _temp + '、'
        return answer

    def query_effect():
        answer = '主治:'
        # temp = query['query'][0]
        # 获取完整的药名
        _name = query_med(query['query'][0])
        if _name:
            pass
        else:
            _name = {'name': query['query'][0]}
            _name = [_name]
        for value in _name:
            # 名称检查
            # for el in _name:
            #     temp = re.match(dict(el['n'])['name'], query['subject'])
            #     if temp:
            #         _name = temp.group()
            temp = query_symptom_by_name(g, value['name'])
            if temp:
                for index, value in enumerate(temp):
                    answer += '(' + str(index + 1) + ')' + dict(value['n'])['name'] + '。'
            else:
                temp = query_name_by_nickname(g, query['query'][0])
                if len(temp) == 1:
                    temp = query_symptom_by_name(g, dict(temp[0]['n'])['name'])
                    if temp:
                        for value in temp:
                            answer += dict(value['n'])['name']
                    #     return answer
                    # else:
                    #     return ''
                else:
                    for index, value in enumerate(temp):
                        temp = query_symptom_by_name(g, dict(value['n'])['name'])
                        for i, v in enumerate(temp):
                            if i == 0:
                                answer += '【' + dict(value['n'])['name'] + '】'
                            answer += '(' + str(i + 1) + ')' + dict(v['n'])['name']
                        answer += '。'
        return answer

    def query_med_inf(self):
        # answer = query_medicine_by_name(g, self)
        temp = query_med(self)
        answer = ''
        if temp:
            for value in temp:
                str1 = ''
                for value in temp:
                    _temp = query_nickname_by_name_and_category(g, value['name'], value['category'])
                    if _temp:
                        str1 = ' 释名: '
                        for el in _temp:
                            str1 += dict(el['n'])['name'] + '、'
                        str1 = str1[:-1] + '。'
                    answer += '【' + value['category'] + value['name'] + '】 ' + str1 + ' 性状:' + value['appearance']
        else:
            answer = ''
        return answer

    select = query['variety']
    if select:
        temp = re.match('什么', query['subject'])
        _temp = ''
        for el in subject:
            __temp = re.match(el, query['verb'])
            if __temp:
                _temp = __temp.group()
        if select == 1:
            if check_object(query['object']):
                return query_effect()
            elif temp or _temp:
                if temp:
                    return query_med_inf(query['object'])
                elif _temp:
                    return query_med_inf(query['subject'])
        elif select == 2:
            # 查询某种病怎么治疗
            if check_verb(query['verb']):
                temp = query_usage_by_symptom(g, query['query'][0])
                if temp:
                    for value in temp:
                        answer += '【' + dict(value['m'])['name'] + '】' + dict(value['n'])['name']
                else:
                    name = query_name_by_symptom(g, query['subject'])
                    answer = '【可用药材】' + query_med_inf(dict(name[0]['n'])['name'])
                return answer
    else:
        for el in name:
            if name.count(query['query'][1]):
                return query_nickname(query['query'][0])
        for el in effect:
            if effect.count(query['query'][1]):
                return query_effect()
        for el in appearance:
            if appearance.count(query['query'][1]):
                str1 = ''
                for value in query_med(query['query'][0]):
                    str1 += '【' + value['category'] + value['name'] + '】' + value['appearance']
                return str1
    print(query)
    return answer


# 根据药名和分类查询昵称
def query_nickname_by_name_and_category(graph, name, category):
    g = graph.run(f"match(m:med)-[r:别名]->(n:med) where m.name='{name}' and m.category='{category}' return n").data()
    return g


# 根据别名和分类查询主名
def query_name_by_nickname_and_category(graph, name, category):
    g = graph.run(f"match(n:med)-[r:别名]->(m:med) where m.name='{name}' and m.category='{category}' return n").data()
    return g


# 根据药名查询药
def query_medicine_by_name(graph, self):
    g = graph.run(f"match(n:med) where n.name=~'.*{self}.*' return n").data()
    return g


# 根据药名查询别称
def query_nickname_by_name(graph, self):
    g = graph.run(f"match(m:med)-[r:别名]->(n:med) where m.name='{self}' return n").data()
    return g


# 根据别称查询主名
def query_name_by_nickname(graph, self):
    g = graph.run(f"match(n:med)-[r:别名]->(m:med) where m.name='{self}' return n").data()
    return g


# 根据药名查询症状
def query_symptom_by_name(graph, self):
    g = graph.run(f"match(m:med)-[r:主治]->(n:symptom) where m.name='{self}' return n").data()
    return g


# 根据症状查询药名
def query_name_by_symptom(graph, self):
    g = graph.run(f"match(n:med)-[r:主治]->(m:symptom) where m.name=~'.*{self}.*' return n").data()
    return g


# 根据药名和分类查询性状
def query_add_by_name_and_category(graph, name, category):
    g = graph.run(f"match(m:med)-[r:性状]->(n:add) where m.name='{name}' and m.category='{category}' return n").data()
    return g


# 根据症状查询用法
def query_usage_by_symptom(graph, symptom):
    g = graph.run(f"match(m:symptom)-[r:用法]->(n:step) where m.name=~'.*{symptom}.*' return m,n").data()
    return g


if __name__ == '__main__':
    # graph = Graph('http://neo4j:root@localhost:7474/')
    # result = query_name_by_nickname(graph, '肉松容')
    # result = result[0]
    # print(dict(result['n']))
    # print(run('桔梗的别名是什么'))
    # print(run('桔梗能治什么病'))
    # print(run('产后腹痛怎么治'))
    # print(run('甘草属于本草纲目中的哪一类'))
    # print(run('甘草主治哪些疾病'))
    # print(run('甘草有什么用'))
    # print(run('腹痛胎动怎么治疗'))
    # print(run('甘草可以治什么病'))
    # print(run('什么是甘草'))
    # print(run('甘草是什么'))
    # print(run('冬瓜的功效如何'))
    # print(run('甘草的性状如何'))
    # print(run('大小便血怎么治'))
    # print(run('什么是叛奴盐'))
    # print(run('地毛能治什么病'))
    # print(run('什么是苦菜'))
    # print(run('什么是黑牛儿'))
    # print(run('黑牛儿有什么用'))
    # print(run('雄黄油有什么效果'))
    #
    # print(run('九真藤能治什么病'))
    #
    # print(run('续根草是什么'))
    # print(run('漏疮脓血怎么治疗'))
    # print(run('黄芪的性状如何'))
    # print(run('甘草的作用是什么'))
    # print(run('鸡肠草是什么'))
    # print(run('白冬瓜有什么用'))
    # print(run('冬瓜有什么用'))
    # print(run('沙角能治什么病'))
    print(run('木患子有什么用'))
