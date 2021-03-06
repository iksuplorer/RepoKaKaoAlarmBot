import httplib2,json,requests
from datetime import datetime, timedelta

def getUrlParser(fav_repository,branch) :
    index = fav_repository.find('github')
    url = fav_repository[index:]
    index = url.find("/")
    url = "https://api.github.com/repos"+url[index:]+"/branches/"+branch
    return url

def getRepositoryInfo(fav_repository,branch,flag) :
    if flag == 1 : url = fav_repository; # 만약 flag가 1이라면 재사용한다
    else : url = getUrlParser(fav_repository,branch) # 만약 flag가 0이라면 새로 구한다
    dataList = [] #0번째는 생성날짜,1번째는 업데이트날짜, 2번째는 git api 주소
    try:
        content = requests.get(url,headers={'Authorization':'token 6f6d00c786cd3662b25716bf6c6fb6a2084f401d'})
        if content.status_code !=200 :
            raise Exception("정상적이지 않은 레파지토리 입니다.")
        jsonObject = json.loads(content.content)
        create_at = jsonObject.get("commit").get("commit").get("committer").get("date")
        updated_at = jsonObject.get("commit").get("commit").get("committer").get("date")
        #create_at = jsonObject.get("commit").get("commit").get("committer").get("date").replace("T"," ").replace("Z","") # 기본적으로 붙어있는 T와 Z를 없앰
        #create_at = datetime.strptime(create_at, "%Y-%m-%d %H:%M:%S") # 날짜 연산을 위해서 dateType으로 형변환
        #updated_at = jsonObject.get("commit").get("commit").get("committer").get("date").replace("T"," ").replace("Z", "") # 기본적으로 붙어있는 T와 Z를 없앰
        #updated_at = datetime.strptime(updated_at, "%Y-%m-%d %H:%M:%S") # 날짜 연산을 위해서 dateType으로 형변환
        #create_at = str(create_at + timedelta(hours=9)).replace("-","").replace(":","").replace(" ","") # 9시간 더한 값 저장
        #updated_at = str(updated_at + timedelta(hours=9)).replace("-","").replace(":","").replace(" ","") # 9시간 더한 값 저장

        dataList.append(create_at) # dataList[0]에다가 깃 생성일 append
        dataList.append(updated_at) # dataList[1]에다가 깃 수정일 append
        dataList.append(url); #dataList[2]에다가 git api 주소를 append
        return dataList # 리스트 반환
    except:
        dataList.append(404) # 예외 발생시 리스트의 0번째 공간은 404를 append
        return dataList # 리스트 반환
