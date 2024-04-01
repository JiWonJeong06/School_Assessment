import csv, random
from tkinter import* 
def next():
    global ANS, score, total, correct, tk
    EN_WORD = random.sample(word, 5)
    ANS = random.randint(0,4)
    en_kr = random.randint(0,1)
    QUE = EN_WORD[ANS][en_kr]
    que_label.config(text=QUE) 
    try: percent = round(100*(correct/total), 2);correctrate_label.config(text=f'정답률: {percent} %')
    except: correctrate_label.config(text=f'정답률: 0%')
    total += 1
    if score >= 100: 
        score = 100
        tk.quit()
        print(f'{score}점까지, 정답률 {percent}%')
    for i in range(5):
        if en_kr == 0: ans_button[i].config(text=EN_WORD[i][1])
        else: ans_button[i].config(text=EN_WORD[i][0])
    
def check(idx):
    global  ANS, score, correct
    idx = int(idx)
    if ANS == idx: correct +=1 ; score += 3;  next()
    else:  score -= 1; score = max(0, score); next()
    score_label.config(text=f'{score} 점')

score = 0 #점수
ANS = 0 #영어 인덱스
total = 0 #문제가 나온 개수
correct = 0 #정답 개수

with open('EN-KR_word.csv', 'r', encoding='UTF8') as word: #영어 파일 열기
    word = list(csv.reader(word))

w,h,fs, f = 30, 2, 20, 'Yu Gothic UI Semibold' #가로,세로,폰트크기,폰트 설정
#타이틀
tk = Tk(); tk.title('영단어 퀴즈')
#점수
tk.config(padx=30, pady=30, bg='#DAD9FF')
score_label = Label(tk,  width=w, height=h, text='0 점', font=(f, fs), bg='#F6F6F6', fg='#000000')
score_label .pack()
#문제
que_label = Label(tk,  width=w, height=h, font=(f, fs), bg='#F6F6F6', fg='#000000')
que_label.pack()
#버튼 답안지
ans_button = []
for i in range(5): 
    button = Button(tk, width=w, height=h, font=(f, fs), bg='#FFD9EC', fg='#000000', command=lambda idx=i: check(idx)) 
    button.pack(); ans_button.append(button)
#정답률
correctrate_label= Label(tk,  width=w, height=h, font=(f, fs), bg='#F6F6F6', fg='#000000')
correctrate_label.pack()
next();tk.mainloop()
