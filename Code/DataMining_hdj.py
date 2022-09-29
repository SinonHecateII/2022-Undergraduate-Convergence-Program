from lib2to3.pgen2 import token
from re import L
import requests
import json
import pymysql
import ImportantData
import time

#MySQL 연결
conn = ImportantData.conn

token = ImportantData.Token_hdj
head = {'Authorization' : 'token %s' % token}

with conn:
    with conn.cursor() as cur:
        sql = "SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE table_schema = 'sys' AND table_name = 'github_db'"  # 테이블의 컬럼명을 가져온다.
        cur.execute(sql)
        result = cur.fetchall()

        LanguageList = []  #처음 실행했을 때 칼럼명을 저장
        for i in range(0, len(result)):
            LanguageList.append(result[i][0])

        i = 4035
        while(i < 40000):
            url = 'https://api.github.com/user/' + str(i)  #id로 유저 이름 찾기
            UrlUser = requests.get(url, headers=head)
            
            text = UrlUser.text
            UserData = json.loads(text)

            try:
                owner = UserData['login']  #유저 이름 가져오기

                url = 'https://api.github.com/users/' + str(owner) + '/repos'
                UrlRepository = requests.get(url, headers=head)

                text = UrlRepository.text
                RepositoryData = json.loads(text)
                for j in range(0, len(RepositoryData)):
                    Repository = RepositoryData[j]  #i번재 레포지스토리
                    RepositoryName = Repository['name']  #해당 유저의 i번째 레포지스토리 이름 가져오기

                    url = 'https://api.github.com/repos/' + str(owner) + '/' + str(RepositoryName)
                    UrlDate = requests.get(url, headers=head) 
                    text = UrlDate.text
                    RepositoryDateData = json.loads(text)  #레포지스토리 날짜
                    create_date = RepositoryDateData['created_at']
                    updated_date = RepositoryDateData['updated_at']
                    pushed_date = RepositoryDateData['pushed_at']

                    url = 'https://api.github.com/repos/' + str(owner) + '/' + str(RepositoryName) + '/languages' 
                    UrlLanguage = requests.get(url, headers=head)
                    text = UrlLanguage.text
                    LanguageData = json.loads(text)
                    
                    LanguageKey = list(LanguageData.keys())  #해당 레포지스토리에 있는 언어 종류 추출
                    
                    if(LanguageKey == []):  #해당 레포지스토리에 언어가 있는지 확인
                        print(str(i) + " | " + owner + "의 " +RepositoryName +"에 언어 데이터가 없어 다음 레포지스토리를 탐색합니다.")
                    else:
                        sql = "INSERT INTO github_db (User_ID, User_Name, Repository_Name, created_at, updated_at, pushed_at) VALUE(%s, %s,%s,%s,%s, %s)"
                        cur.execute(sql, (str(i), owner, RepositoryName, str(create_date), str(updated_date), str(pushed_date)))
                        conn.commit()

                        for k in range(0, len(LanguageKey)):                        
                            if LanguageKey[k] not in LanguageList:  #해당 이름의 칼럼이 리스트에 존재하지 않는다면
                                if(str.isalnum(LanguageKey[k]) == False):  #C++과 같은 특수문자인지 검사
                                    sql = "ALTER TABLE github_db add `" + LanguageKey[k] + "` int NOT NULL default '0'"
                                else:
                                    sql = "ALTER TABLE github_db add " + LanguageKey[k] + " int NOT NULL default '0'"
                                cur.execute(sql)
                                conn.commit()
                                LanguageList.append(LanguageKey[k])

                            #해당 언어 Byte 수 삽입    
                            if(str.isalnum(LanguageKey[k]) == False):
                                sql = "UPDATE github_db SET `" + LanguageKey[k] + "`=%s WHERE User_Name=%s AND Repository_Name=%s"
                            else:
                                sql = "UPDATE github_db SET " + LanguageKey[k] + "=%s WHERE User_Name=%s AND Repository_Name=%s"
                            cur.execute(sql,(LanguageData[LanguageKey[k]], owner, RepositoryName))
                            conn.commit()
                        print(str(i) + " | " + owner + "의 " +RepositoryName +"정보를 성공적으로 저장하였습니다.")
                i = i + 1
            except:
                url = 'https://api.github.com/rate_limit' 
                UrlLimit = requests.get(url, headers=head)
                text = UrlLimit.text
                Limit = json.loads(text)
                resource = Limit['resources']
                remain = resource['core']
                if(remain['remaining'] == 0):  #API 사용횟수가 다 끝났다면
                    print("API 사용횟수가 끝나 10분 대기합니다. (시간당 5000회)")
                    time.sleep(60)

                    url = 'https://api.github.com/rate_limit' 
                    UrlLimit = requests.get(url, headers=head)
                    text = UrlLimit.text
                    Limit = json.loads(text)
                    resource = Limit['resources']
                    remain = resource['core']
                    if(remain['remaining'] != 0):  
                        i = i + 1
                    continue

                print(str(i) + " | 다음 owner의 레포지스토리를 탐색합니다. ")
                i = i + 1


