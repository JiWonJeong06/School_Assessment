import pygame, random ,requests
from bs4 import BeautifulSoup
#게임 초기화
pygame.init()
#이미지,사진
m_list = []
f = open("movie\영화리스트.txt", 'r', encoding='UTF-8')
while True:
    line = f.readline()
    m_list.append(line.strip('\n'))
    if not line: break
del m_list[-1]
f.close()
ran_choice = random.choice(m_list)
puzzleImage = pygame.image.load(f"movie\{ran_choice}.jpg")
puzzleSize = puzzleImage.get_size()
puzzleSize = (620, 880)
puzzleImage = pygame.transform.smoothscale(puzzleImage,puzzleSize)
#영화 정보
url = requests.get('https://movie.naver.com/movie/bi/mi/basic.naver?code='+ ran_choice)
url.text
soup = BeautifulSoup(url.content , "html.parser")
soup_list1 = soup.find('h3',{'class':'h_movie'}).find('a')
soup_list2 = soup.find('dl',{'class':'info_spec'}).find_all('a')
soup_list3 = soup.find('div',{'class':'video'}).find('div',{'class':'story_area'})
for h3 in soup_list1:   
    print(h3.text)
for a in soup_list2:   
    print(a.text)
for div in soup_list3:
    print(div.text)
#그림판
sc_wh = 4
iNum, jNum =  sc_wh, sc_wh
puzzle_list = []
puzzle_list_init = []
for i in range(iNum):
    tempList = []
    tempListInit = []
    for j in range(jNum):
        w,h = puzzleSize[0]/iNum, puzzleSize[1]/jNum
        x,y = i*w, j*h
        partImage = puzzleImage.subsurface((x,y,w,h))        
        tempDict = {
            "num":j*jNum+i+1,
            "image":partImage,
            "pos":(x,y)
        }
        tempList.append(tempDict)
        tempListInit.append(j*jNum+i+1)
    puzzle_list.append(tempList)
    puzzle_list_init.append(tempListInit)
puzzle_list[-1][-1]["num"] = 0
puzzle_list_init[-1][-1] = 0
bs = pygame.Surface((w,h))
bs.fill((0,0,0))
puzzle_list[-1][-1]["image"] = bs
#해상도
size = puzzleSize
screen = pygame.display.set_mode(size)
#제목
title = "영화 퍼즐맞추기"
pygame.display.set_caption(title)
#FPS설정
clock = pygame.time.Clock()
#색
black = (0,0,0)
white = (255,255,255)
#방향키
dirDict = {
    "left":(-1,0), "right":(1,0),
    "up":(0,-1), "down":(0,1)
}
keyPress = False
mix = False
gameOver = False
spaceNum = 0
run = True
#게임 시작하기
while run:
    #FPS 설정
    clock.tick(60)
    #섞기
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            keyName = pygame.key.name(event.key)
            if keyName == "space":
                mix = not mix
                spaceNum += 1
            for key in dirDict.keys():
                if key == keyName:
                    keyPress = True
    #입력
    for i in range(iNum):
        for j in range(jNum):
            if puzzle_list[i][j]["num"] == 0:
                blank =(i,j)
    # 바꾸기
    if keyPress == True or mix == True:
        if mix == True:
            ranIndex = random.randrange(0,4)
            keyName = list(dirDict.keys())[ranIndex]
        i, j = blank
        ii, jj = dirDict[keyName]
        iNew, jNew= i+ii, j+jj
        if iNew>=0 and iNew<iNum and jNew>=0 and jNew<jNum:
            puzzle_list[i][j]["num"], puzzle_list[iNew][jNew]["num"] = \
                puzzle_list[iNew][jNew]["num"], puzzle_list[i][j]["num"] 
            puzzle_list[i][j]["image"], puzzle_list[iNew][jNew]["image"] = \
                puzzle_list[iNew][jNew]["image"], puzzle_list[i][j]["image"]                
        keyPress = False
    # 게임 종료 조건
    if spaceNum >= 2:
        same = True
        for i in range(iNum):
            for j in range(jNum):
                if puzzle_list[i][j]["num"] != puzzle_list_init[i][j]:
                    same = False
        if same == True:
            gameOver = True
    # 퍼즐 그리기
    for i in range(iNum):
        for j in range(jNum):
            img = puzzle_list[i][j]["image"]
            pos = puzzle_list[i][j]["pos"]
            screen.blit(img, pos)
            x,y = pos
            A = (x, y)
            B = (x+w, y)
            C = (x, y+h)
            D = (x+w, y+h)
            pygame.draw.line(screen,white,A,B,2)  
            pygame.draw.line(screen,white,A,C,2)  
            pygame.draw.line(screen,white,D,B,2)  
            pygame.draw.line(screen,white,D,C,2)  
    if gameOver == True or spaceNum >= 3:
        screen.blit(puzzleImage,(0,0))
    #게임 보여주기
    pygame.display.update()
#게임 종료
pygame.quit()
