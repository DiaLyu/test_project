
# синтаксические правила для вывода строк с связанными именами и городами
class SyntaxParse:

     def __init__(self, syntaxStructure):
          self.syntaxStructure = syntaxStructure
          self.headIdList = [token.head_id for token in syntaxStructure]


     def phrases(self):
          all_phrases = []
          tokens = self.syntaxStructure

          connect_words = []
          for i in range(len(tokens)):
               properties = [{"id": tokens[j].id, "rel": tokens[j].rel, "index": j} for j in range(len(tokens)) if tokens[j].head_id == tokens[i].id]
               connect_words.append(properties)

          phrases = self.rule_5(connect_words, "root", "advcl", "obl", "case", "nsubj", "flat:name")
          if not phrases:
               phrases = self.rule_6(connect_words, "root", "nsubj", "appos", "flat:name", "obl", "case")

          if not phrases:
               phrases = self.rule_3(connect_words, "root", "nsubj", "conj", "obl", "case")
          
          if not phrases:
               phrases = self.rule_3(connect_words, "ccomp", "nsubj", "advcl", "obl", "case")

          if not phrases:
               phrases = self.rule_4(connect_words, "root", "obl", "case", "nmod", "flat:name")

          if not phrases:
               phrases = self.rule_1(connect_words, "root", "nsubj", "flat:name", "obl", "case")

          if not phrases:
               phrases = self.rule_1(connect_words, "root", "nsubj", "nmod", "obl", "case")

          if not phrases:
               phrases = self.rule_1(connect_words, "root", "nsubj", "appos", "obl", "case")

          if not phrases:
               phrases = self.rule_2(connect_words, "advcl", "nsubj", "obl", "case")

          if not phrases:
               phrases = self.rule_2(connect_words, "root", "nsubj", "obl", "case")

          if not phrases:
               phrases = self.rule_2(connect_words, "root", "obj", "obl", "case")

          # for phrase in phrases:
          #      str_phrase = ""
          #      for token in phrase:
          #           str_phrase += token.text + " "
          #      all_phrases.append(str_phrase)
          return phrases


     # self.rule_1 = ["root", ["nsubj", "flat:name"], ["obl", "case"]]
     # self.rule_6 = ["root", ["nsubj", "nmod"], ["obl", "case"]]
     # self.rule_10 = ["root", ["nsubj", "appos"], ["obl", "case"]]
     def rule_1(self, connect_words, *rels):
          phrases = []
          tokens = self.syntaxStructure

          for i in range(len(tokens)):
               is_rule_1 = [False, False]
               name_city = {}
               if tokens[i].rel == rels[0]:
                    nameHero = []
                    cityHero = []
                    for property in connect_words[i]:
                         if property['rel'] == rels[1]:
                              nameHero.append(tokens[property["index"]])
                              for nam in connect_words[property["index"]]:
                                   if nam['rel'] == rels[2]:
                                        nameHero.append(tokens[nam["index"]])  
                                        nameHero = sorted(nameHero, key=lambda x: x.start)
                                        is_rule_1[0] = True


                         if property['rel'] == rels[3]:
                              cityHero.append(tokens[property["index"]])
                              for case in connect_words[property["index"]]:
                                   if case['rel'] == rels[4]:
                                        cityHero.append(tokens[case["index"]])  
                                        cityHero = sorted(cityHero, key=lambda x: x.start)
                                        is_rule_1[1] = True
                    if all(is_rule_1):
                         name_city = {"Name": nameHero, "City": cityHero}
                         phrases.append(name_city)
          return phrases
     

     # self.rule_2 = ["advcl", ["nsubj"], ["obl", "case"]]
     # self.rule_3 = ["root", ["nsubj"], ["obl", "case"]]
     # self.rule_5 = ["root", ["obj"], ["obl", "case"]]
     def rule_2(self, connect_words, *rels):
          phrases = []
          tokens = self.syntaxStructure

          for i in range(len(tokens)):
               is_rule_1 = [False, False]
               name_city = {}
               if tokens[i].rel == rels[0]:
                    nameHero = []
                    cityHero = []
                    for property in connect_words[i]:
                         if property['rel'] == rels[1]:
                              nameHero.append(tokens[property["index"]])
                              is_rule_1[0] = True

                         if property['rel'] == rels[2]:
                              cityHero.append(tokens[property["index"]])
                              for case in connect_words[property["index"]]:
                                   if case['rel'] == rels[3]:
                                        cityHero.append(tokens[case["index"]])
                                        cityHero = sorted(cityHero, key=lambda x: x.start)
                                        is_rule_1[1] = True

                    if all(is_rule_1):
                         name_city = {"Name": nameHero, "City": cityHero}
                         phrases.append(name_city)
          return phrases
     

     # self.rule_7 = ["root", ["nsubj"], ["conj", "obl", "case"]]
     # self.rule_8 = ["ccomp", ["nsubj"], ["advcl", "obl", "case"]]
     def rule_3(self, connect_words, *rels):
          phrases = []
          tokens = self.syntaxStructure

          for i in range(len(tokens)):
               is_rule_1 = [False, False]
               name_city = {}
               if tokens[i].rel == rels[0]:
                    nameHero = []
                    cityHero = []
                    for property in connect_words[i]:
                         if property['rel'] == rels[1]:
                              nameHero.append(tokens[property["index"]]) 
                              is_rule_1[0] = True

                         if property['rel'] == rels[2]:
                              for obl in connect_words[property["index"]]:
                                   if obl['rel'] == rels[3]:
                                        cityHero.append(tokens[obl["index"]])  
                                        for case in connect_words[obl["index"]]:
                                             if case['rel'] == rels[4]:
                                                  cityHero.append(tokens[case["index"]])
                                                  cityHero = sorted(cityHero, key=lambda x: x.start)
                                                  is_rule_1[1] = True

                    if all(is_rule_1):
                         name_city = {"Name": nameHero, "City": cityHero}
                         phrases.append(name_city)
          return phrases


     # self.rule_4 = ["root", ["obl", ["case"], ["nmod", "flat:name"]], ["obl", "case"]]
     def rule_4(self, connect_words, *rels):
          phrases = []
          tokens = self.syntaxStructure

          for i in range(len(tokens)):
               is_rule_1 = [False, False]
               name_city = {}
               if tokens[i].rel == rels[0]:
                    nameHero = []
                    cityHero = []
                    for property in connect_words[i]:
                         if property['rel'] == rels[1]:
                              cityHero.append(tokens[property["index"]])
                              for property_1 in connect_words[property["index"]]:
                                   if property_1['rel'] == rels[2]:
                                        cityHero.append(tokens[property_1["index"]])
                                        cityHero = sorted(cityHero, key=lambda x: x.start)
                                        is_rule_1[0] = True

                                   if property_1['rel'] == rels[3]:
                                        for nam in connect_words[property_1["index"]]:
                                             if nam['rel'] == rels[4]:
                                                  nameHero.append(tokens[nam["index"]])
                                                  is_rule_1[1] = True

                    if all(is_rule_1):
                         name_city = {"Name": nameHero, "City": cityHero}
                         phrases.append(name_city)
          return phrases
     

     # self.rule_9 = ["root", ["advcl", "obl", "case"], ["nsubj", "flat:name"]]
     def rule_5(self, connect_words, *rels):
          phrases = []
          tokens = self.syntaxStructure

          for i in range(len(tokens)):
               is_rule_1 = [False, False]
               name_city = {}
               if tokens[i].rel == rels[0]:
                    nameHero = []
                    cityHero = []
                    for property in connect_words[i]:
                         if property['rel'] == rels[1]:
                              for obl in connect_words[property["index"]]:
                                   if obl['rel'] == rels[2]:
                                        cityHero.append(tokens[obl["index"]])  
                                        for case in connect_words[obl["index"]]:
                                             if case['rel'] == rels[3]:
                                                  cityHero.append(tokens[case["index"]])
                                                  cityHero = sorted(cityHero, key=lambda x: x.start)
                                                  is_rule_1[0] = True

                         if property['rel'] == rels[4]:
                              nameHero.append(tokens[property["index"]])
                              for nam in connect_words[property["index"]]:
                                   if nam['rel'] == rels[5]:
                                        nameHero.append(tokens[nam["index"]])  
                                        nameHero = sorted(nameHero, key=lambda x: x.start)
                                        is_rule_1[1] = True

                    if all(is_rule_1):
                         name_city = {"Name": nameHero, "City": cityHero}
                         phrases.append(name_city)
          return phrases
     
     # ["root", ["nsubj", "appos", ["flat:name"], ["flat:name"]], ["obl", "case"]]
     def rule_6(self, connect_words, *rels):
          phrases = []
          tokens = self.syntaxStructure

          for i in range(len(tokens)):
               is_rule_1 = [False, False]
               name_city = {}
               if tokens[i].rel == rels[0]:
                    nameHero = []
                    cityHero = []
                    for property in connect_words[i]:
                         if property['rel'] == rels[1]:
                              for obl in connect_words[property["index"]]:
                                   if obl['rel'] == rels[2]:
                                        nameHero.append(tokens[obl["index"]])  
                                        names = connect_words[obl["index"]]
                                        for j in range(len(names)):
                                             if j != len(names) - 1:
                                                  if names[j]['rel'] == rels[3] and names[j+1]['rel'] == rels[3]:
                                                       nameHero.append(tokens[names[j]["index"]])
                                                       nameHero.append(tokens[names[j + 1]["index"]])
                                                       nameHero = sorted(nameHero, key=lambda x: x.start)
                                                       is_rule_1[0] = True

                         if property['rel'] == rels[4]:
                              cityHero.append(tokens[property["index"]])
                              for nam in connect_words[property["index"]]:
                                   if nam['rel'] == rels[5]:
                                        cityHero.append(tokens[nam["index"]])
                                        cityHero = sorted(cityHero, key=lambda x: x.start)
                                        is_rule_1[1] = True

                    if all(is_rule_1):
                         name_city = {"Name": nameHero, "City": cityHero}
                         phrases.append(name_city)
          return phrases
