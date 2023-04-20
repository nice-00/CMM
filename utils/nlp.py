import os.path

import hanlp
import re


def nlp(api, self):
    result = dict(api(self, tasks=['tok/fine', 'pos/ctb', 'srl', 'con']))
    return result


def run(question):
    Hanlp = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH)  # 世界最大中文语料库
    result = nlp(Hanlp, question)
    noun = []
    verb = ''
    verb_position = 0
    subject = ''
    _object = ''
    match = []
    variety = 0
    with open(os.path.dirname(__file__) + "/data/action.txt", "r", encoding='UTF-8') as file:
        action = file.readlines()
        action = [x.strip() for x in action]
        file.close()
    # 清洗语义结果
    result['srl'] = result['srl'][len(result['srl']) - 1]
    # 理解意图
    # 提取主语/对象
    for index, el in enumerate(result['pos/ctb']):
        if el == 'NN' or el == 'PN' or el == 'NR':
            noun.append(result['tok/fine'][index])
    # 提取谓语
    for index, el in enumerate(result['srl']):
        if el[1] == "PRED":
            verb = el[0]
            verb_position = index
            subject = result['srl'][0][0]
            if index < len(result['srl']) - 1 and action:
                _object = result['srl'][index + 1][0]
    # 句式判断
    # for el in noun:
    #     temp = re.search(el, subject)
    #     if temp:
    #         # match.append(temp.group())
    #         # _temp = ""
    #         temp = temp.group()
    for value in result['srl']:
        if value[0] == verb:
            for index, _el in enumerate(result['tok/fine']):
                if _el == verb:
                    _temp = result['pos/ctb']
                    __temp = result['tok/fine']
                    str1 = ''
                    for _index, _value in enumerate(_temp):
                        if _value == 'NN' or _value == 'NR' or _value == 'PN':
                            str1 += __temp[_index]
                        elif _index == index:
                            break
                    not_find = re.search(str1, question)
                    not_find = False if not_find else True
                    if str1 != subject and  not_find:
                        for _value in noun:
                            temp = re.search(_value, subject)
                            if temp:
                                match.append(temp.group())
                        break
                    else:
                        match.append(subject)
                        variety = 1
            match.append(verb + _object)
        elif value[1] == 'ARGM-ADV':
            match.append(subject)
            match.append(verb)
            variety = 2
            break
            # if len(match) > 2:
            #     # for value in match:
            #     #     _temp += value
    if match:
        if len(match) < 2:
            variety = 1
            match.append(verb + _object)
    else:
        variety = 2
        _temp = ''
        for value in result['srl']:
            if value[1] != 'ARGM-ADV':
                _temp += value[0]
            else:
                break
        match.append(_temp)
        match.append(verb)
        subject = _temp
    temp = re.match(match[0], subject)
    if temp:
        _temp = re.match(match[0], subject)
        if _temp:
            match[0] = _temp.group()
    else:
        _temp = re.search('.' + match[0], subject)
        if _temp:
            match[0] = _temp.group()
    match = {'query': match, 'subject': subject, 'verb': verb if variety else '', 'object': _object if variety else '',
             'variety': variety}
    # print(subject, verb, noun, match)
    # for el in result:
    #     print(el, ":\t", result[el])
    return match

# if __name__ == "__main__":
#     run('桔梗的别名是什么')
#     print('\n\n')
#     run('桔梗能治什么病')
#     print('\n\n')
#     run('痰嗽喘急怎么治')
#     print('\n\n')
#     run('甘草属于本草纲目中的哪一类')
#     print('\n\n')
#     run('甘草主治哪些疾病')
#     print('\n\n')
#     run('甘草有什么用')
#     print('\n\n')
#     run('心腹胀满怎么治疗')
#     print('\n\n')
#     run('甘草可以治什么病')
#     print('\n\n')
#     run('甘草的作用是什么')
#     print('\n\n')
#     run('甘草的功效如何')
# run('白瓜子的功效如何')
# str1 = "白瓜子（冬瓜仁）"
# print(re.match('白瓜子', str1).group())
