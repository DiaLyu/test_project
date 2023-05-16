import json
import pymorphy2
import nltk
from nltk.tokenize import WordPunctTokenizer, sent_tokenize, word_tokenize
from natasha import (
    Segmenter,
    MorphVocab,
    
    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    Doc
)
from analyzeBook.syntaxParse import SyntaxParse
import pathlib
from pathlib import Path

class AnalyzeText:

    segmenter = Segmenter()
    morph_vocab = MorphVocab()

    emb = NewsEmbedding()
    morph_tagger = NewsMorphTagger(emb)
    syntax_parser = NewsSyntaxParser(emb)
    ner_tagger = NewsNERTagger(emb)

    tokenizer=WordPunctTokenizer()
    morph = pymorphy2.MorphAnalyzer()

    def __init__ (self, file_path):
        self.file_path = file_path


    def analyze(self):
        # получаем данные из других файлов
        move_words = self.open_file_move()
        text_book = self.open_file_book()
        name_countries, city_counties = self.open_file_cities()

        doc = self.process_text(text_book)
        loc_spans, per_spans = self.get_names_cities(doc)

        # страны-города в тексте
        result_cities = self.get_cities_text(name_countries, city_counties, loc_spans)

        routes = self.get_routes(doc, per_spans, result_cities, move_words)

        return routes


    def open_file_move(self):
        move_words = []
        path = Path(pathlib.Path.cwd(), 'analyzeBook', 'static', '2.txt')
        with open(path, encoding='utf-8') as movement:
            for line in movement:
                move_words = line.split()
        return move_words
    

    def open_file_book(self):
        lst = []
        text_lst = ""
        # ../books/Voina_i_mir.txt
        with open(self.file_path , encoding='utf-8') as text_book:
            for line in text_book:
                try:
                    line_text = line.strip()
                    if line_text != "":
                        lst.append(line_text)
                        text_lst += line_text + ' '
                except UnicodeEncodeError:
                    pass
        return text_lst
    
    
    def open_file_cities(self):
        path = Path(pathlib.Path.cwd(), 'analyzeBook', 'static', 'cities.json')
        with open(path, 'r', encoding='utf-8') as read_json:
            data_countries = json.load(read_json)

        name_countries = []         # названия стран
        city_counties = []          # список массивов городов по странам
        for obj in data_countries:
            name_countries.append(obj['country']['name'])
            cities = []
            for obj_cit in obj['country']['cities']:
                for city in obj_cit:
                    cities.append(city.lower())
            city_counties.append(cities)

        for name in name_countries:
            name = list(map(lambda x: x.replace('ё','е'), name))

        for city in city_counties:
            city = list(map(lambda x: x.replace('ё','е'), city))

        return name_countries, city_counties
    

    def process_text(self, text):
        doc = Doc(text)
        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)
        doc.tag_ner(self.ner_tagger)

        for span in doc.spans:
            span.normalize(self.morph_vocab)

        for token in doc.tokens:
            token.lemmatize(self.morph_vocab)

        return doc


    def get_names_cities(self, doc):
        loc_spans = []
        per_spans = []
        for span in doc.spans:
            if span.type == 'LOC':
                normal_word = span.normal.lower()
                # извлечение из морфологического разбора слова существительное в именительном падеже
                loc_spans.append(self.morph_vocab.lemmatize(normal_word, 'NOUN', {'Animacy': 'Inan', 'Case': 'Nom'}))
            if span.type == 'PER':
                tokens = span.tokens
                flg = True
                for token in tokens:    # 
                    if token.pos != 'PROPN':
                        flg = False
                    if ('Animacy' in token.feats) and ('Number' in token.feats):
                        if token.feats['Animacy'] != 'Anim' and token.feats['Number'] != 'Sing':
                            flg = False
                if flg:               
                    per_spans.append(span.normal)

        loc_spans = list(set(loc_spans))
        per_spans = list(set(per_spans))

        return loc_spans, per_spans


    # приведение к нормальной форме ФИО
    def normalFormFIO(self, per_spans):

        result_charact = []

        fio = [['Name', 'Surn'], ['Name', 'Patr'], ['Name', 'Patr', 'Surn'], ['Surn', 'Name', 'Patr']]
        for pers in per_spans:
            final_name = {}
            tokens = self.tokenizer.tokenize(pers)
            for tkn in tokens:
                p = self.morph.parse(tkn)
                # print(p)
                cont_flag = False
                for pars in p:
                    if 'Surn' in pars.tag:
                        final_name['Surn'] = pars.normal_form
                        final_name['gend_surn'] = pars.tag.gender
                        cont_flag = True
                    elif 'Name' in pars.tag:
                        final_name['Name'] = pars.normal_form
                        final_name['gend'] = pars.tag.gender
                        cont_flag = True
                    elif 'Patr' in pars.tag:
                        final_name['Patr'] = pars.normal_form
                        final_name['gend_patr'] = pars.tag.gender
                        cont_flag = True

                    if cont_flag:
                        break

            list_key = list(final_name)
            # в случаях, если повторяются имена, фамилии, отчества, или они не в стандартном порядке, то разделяем их
            if final_name:
                if len(list_key) == 4 and not ((list_key[0] == fio[0][0] and list_key[2] == fio[0][1]) or (list_key[0] == fio[1][0] and list_key[2] == fio[1][1])):
                    name_pers = {list_key[0]: final_name[list_key[0]], list_key[1]: final_name[list_key[1]]}
                    last_pers = {list_key[2]: final_name[list_key[2]], list_key[3]: final_name[list_key[3]]}
                    result_charact.append(name_pers)
                    result_charact.append(last_pers)

                elif len(list_key) == 6 and not ((list_key[0] == fio[2][0] and list_key[2] == fio[2][1] and list_key[4] == fio[2][2]) or (list_key[0] == fio[3][0] and list_key[2] == fio[3][1] and list_key[4] == fio[3][2])):
                    first_pers = {list_key[0]: final_name[list_key[0]], list_key[1]: final_name[list_key[1]]}
                    second_pers = {list_key[2]: final_name[list_key[2]], list_key[3]: final_name[list_key[3]]}
                    third_pers = {list_key[4]: final_name[list_key[4]], list_key[5]: final_name[list_key[5]]}
                    result_charact.append(first_pers)
                    result_charact.append(second_pers)
                    result_charact.append(third_pers)

                else:
                    result_charact.append(final_name)

        normal_list = []

        for charact in result_charact:
            full_name = ""
            not_normal_name = ""
            if 'Name' in charact and 'Surn' in charact and 'Patr' in charact:
                for key in charact:
                    if (key == 'Name' or key == 'Surn' or key == 'Patr'):
                        not_normal_name += charact[key] + " "
                        parse_name = self.morph.parse(charact[key])[0].inflect({'sing', 'nomn', charact['gend']})
                        if parse_name != None:
                            if parse_name.word == 'марь':
                                full_name += parse_name.word + 'я '
                            else:
                                if (parse_name.word == 'ростов' or parse_name.word == 'ахросимов') and charact['gend_surn'] == 'femn':
                                    parse_name.word += 'а'
                                full_name += parse_name.word + " "
                        else:
                            full_name += charact[key] + " "
                
            elif 'Name' in charact and 'Surn' in charact:
                for key in charact:
                    if (key == 'Name' or key == 'Surn'):
                        not_normal_name += charact[key] + " "
                        parse_name = self.morph.parse(charact[key])[0].inflect({'sing', 'nomn', charact['gend']})
                        if parse_name != None:
                            if parse_name.word == 'марь':
                                full_name += parse_name.word + 'я '
                            else:
                                if (parse_name.word == 'ростов' or parse_name.word == 'ахросимов') and charact['gend_surn'] == 'femn':
                                    parse_name.word += 'а'
                                full_name += parse_name.word + " "
                        else:
                            full_name += charact[key] + " "
            elif 'Name' in charact and 'Patr' in charact:
                for key in charact:
                    if (key == 'Name' or key == 'Patr'):
                        not_normal_name += charact[key] + " "
                        parse_name = self.morph.parse(charact[key])[0].inflect({'sing', 'nomn', charact['gend']})
                        if parse_name != None:
                            if parse_name.word == 'марь':
                                full_name += parse_name.word + 'я '
                            else:
                                full_name += parse_name.word + " "
                        else:
                            full_name += charact[key] + " "

            elif 'Name' in charact:
                not_normal_name += charact['Name']
                parse_name = self.morph.parse(charact['Name'])[0].inflect({'sing', 'nomn', charact['gend']})
                if parse_name != None:
                    if parse_name.word == 'марь':
                        full_name += parse_name.word + 'я'
                    else:
                        full_name += parse_name.word
                else:
                    full_name += charact['Name']

            elif 'Surn' in charact and charact['gend_surn'] != None:
                not_normal_name += charact['Surn']
                parse_name = self.morph.parse(charact['Surn'])[0].inflect({'sing', 'nomn', charact['gend_surn']})
                if parse_name != None:
                    if (parse_name.word == 'ростов' or parse_name.word == 'ахросимов') and charact['gend_surn'] == 'femn':
                        parse_name.word += 'а'
                    full_name += parse_name.word
                else:
                    full_name += charact['Surn']
            elif 'Patr' in charact and charact['gend_patr'] != None:
                not_normal_name += charact['Patr']
                parse_name = self.morph.parse(charact['Patr'])[0].inflect({'sing', 'nomn', charact['gend_patr']})
                if parse_name != None:
                    full_name += parse_name.word
                else:
                    full_name += charact['Patr']
                
            if len(full_name.strip()) > 1:
                normal_list.append({"full_name": full_name.strip(), "not_normal_name": not_normal_name.strip()})

        normal_list = list({v["not_normal_name"]:v for v in normal_list}.values())

        return normal_list
    

    def get_cities_text(self, name_countries, city_counties, loc_spans):
        result_cities = []
        # если страна в тексте упоминается, но не названо ни одного города в ней, то в список мест войдет название страны
        for i in range(len(name_countries)):
            list_cities = set(city_counties[i]) & set(loc_spans)
            list_names = set(name_countries[i]) & set(loc_spans)
            if list_cities:
                result_cities.extend(list(list_cities)) 
            elif list_names:
                result_cities.extend(list(list_names))

        # print(result_cities)        # итоговый список городов
        return result_cities

    
    def get_routes(self, doc, per_spans, result_cities, move_words):
        normal_names = self.normalFormFIO(per_spans)

        not_norm_name = [names["not_normal_name"] for names in normal_names]
        full_names = [names["full_name"] for names in normal_names]

        sents = doc.sents
        past_end_word = ['л', 'ла', 'ли', 'шел', 'лся', 'лись', 'лась', 'вшись', 'в']

        routes_hero = []

        for i in range(len(sents)):
            snt = sents[i]
            process = False

            index = 0
            for token in snt.tokens:
                if 'ROMN' in self.morph.parse(token.text)[0].tag:
                    snt.tokens.remove(token)

                elem = any([token.text.endswith(ends) for ends in past_end_word])
                for move in move_words:
                    if (token.lemma == move) and elem:
                        if index != 0:
                            if snt.tokens[index - 1].text != 'не':
                                process = True

                index += 1

            if process:
                tk = SyntaxParse(snt.tokens)    
                phrase = tk.phrases()
                for phr in phrase:
                    city = ' '.join([tkn.lemma for tkn in phr['City']])
                    for res in result_cities:
                        if res in city:
                            str_name = ""
                            nameFIO = phr['Name']
                            pron = [token for token in nameFIO if token.pos == 'PRON']
                            if pron == []:
                                list_names = self.normalFormFIO([' '.join([token.lemma for token in nameFIO])])
                                list_name_full = [names["full_name"] for names in list_names]
                                if list_name_full != []:
                                    str_name = list_name_full[0]
                            else:
                                if i != 0:
                                    iter = 1
                                    while str_name == "" and i - iter >= 0:
                                        last_sent = ' '.join([token.lemma for token in sents[i-iter].tokens])
                                        for ind in range(len(not_norm_name)):
                                            if not_norm_name[ind] in last_sent:
                                                str_name = full_names[ind]
                                        iter += 1
                            if str_name != "":
                                routes_hero.append({'Name': str_name, 'City': res})

        routes = []
        for route in routes_hero:
            flag = True
            for name_route in routes:
                if name_route['Name'] == route['Name']:
                    if name_route['Route'][len(name_route['Route']) - 1] != route['City']:
                        name_route['Route'].append(route['City'])
                    flag = False
            if flag:
                routes.append({'Name': route['Name'], 'Route': [route['City']]})     

        return routes

# analyzeText = AnalyzeText('../books/Voina_i_mir.txt')
# print(analyzeText.analyze())

# print("\n---------------\n")

# analyzeText = AnalyzeText('../books/lermontov1.txt')
# print(analyzeText.analyze())