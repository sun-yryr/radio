# -*- coding: utf-8 -*-
import requests
import json
import re
import os
import lib.functions as f
import datetime as DT

class onsen:
    def __init__(self, keywords, SAVEROOT, dbx):
        self.change_keywords(keywords)
        self.SAVEROOT = SAVEROOT
        self.dbx = dbx
        self.reload_date = DT.date.today()

    def change_keywords(self, keywords):
        if bool(keywords):
            word = "("
            for keyword in keywords:
                word += keyword
                word += "|"
            word = word.rstrip("|")
            word += ")"
            print(word)
            self.isKeyword = True
            self.keyword = re.compile(word)
        else:
            self.isKeyword = False

    def rec(self):
        self.reload_date = DT.date.today()
        res = requests.get("http://www.onsen.ag/api/shownMovie/shownMovie.json")
        res.encoding = "utf-8"
        programs = json.loads(res.text)
        returnData = []
        for program in programs["result"]:
            url = "http://www.onsen.ag/data/api/getMovieInfo/%s" % program
            res2 = requests.get(url)
            prog = json.loads(res2.text[9:len(res2.text)-3])
            title = prog.get("title")
            personality = prog.get("personality")
            update_DT = prog.get("update")
            count = prog.get("count")
            if (title is not None and personality is not None and update_DT !=""):
                if (self.keyword.search(title) or self.keyword.search(personality)):
                    movie_url = prog["moviePath"]["pc"]
                    if (movie_url == ""):
                        continue
                    # フォルダの作成
                    dir_path = self.SAVEROOT + "/" + title.replace(" ", "_")
                    f.createSaveDir(dir_path)
                    # ファイル重複チェック
                    file_name = title.replace(" ", "_") +"#"+ count + ".mp3"
                    file_path = dir_path +"/"+ file_name
                    if not file_name in os.listdir(dir_path):
                        print(prog["update"], prog["title"], prog["personality"])
                        returnData.append(title)
                        res3 = requests.get(movie_url)
                        fs = open(file_path, "wb")
                        fs.write(res3.content)
                        fs.close()
                        dbx_path = "/radio/" + title
                        res = self.dbx.files_list_folder('/radio')
                        db_list = [d.name for d in res.entries]
                        if not title in db_list:
                            self.dbx.files_create_folder(dbx_path)
                        dbx_path += "/" +title+"#"+count+ ".mp3"
                        self.dbx.files_upload(res3.content, dbx_path)
        return returnData

import dropbox
if __name__ == "__main__":
    config = f.load_configurations("./conf/config.json")
    dbx = dropbox.Dropbox(config["all"]["dbx_token"])
    Onsen = onsen(config["Onsen"]["keywords"], "./savefile", dbx)
    a = Onsen.rec()