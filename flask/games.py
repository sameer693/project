#process the input and give outpu
#input if zero mean null [1:stone,2:paper,3scissor}
def st_pa_sc(check):
    try:
        if check[0]["input_1"]==0 or check[0]["input_2"]==0:
            return "waiting for your and your friend's input",0
        elif check[0]["input_1"]==check[0]["input_2"]:
            return "same input",9
        elif (check[0]["input_1"]==1 and check[0]["input_2"]==3) or (check[0]["input_1"]==2 and check[0]["input_2"]==1) or (check[0]["input_1"]==3 and check[0]["input_2"]==2):
            return "player1 won",1
        elif (check[0]["input_1"]==1 and check[0]["input_2"]==2) or (check[0]["input_1"]==2 and check[0]["input_2"]==3) or (check[0]["input_1"]==3 and check[0]["input_2"]==1):
            return "player2 won",2         
    except:
        return "unexpected err",400