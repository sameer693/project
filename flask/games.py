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

def oddeve(check):
    #won by 1,won by 2,0 standby,5 all out
    # 3 -wicket,4 add run
    try:
        if check[0]["innings"]==1:
            #to check if target is set by other player and reached       
            if check[0]["run2"]!=0:
                if check[0]["run2"]==check[0]["run1"]:
                    return "match won by 1st player",1
                elif check[0]["wicket1"]==0:
                    return "all out match won by 2nd player",2 
            elif check[0]["wicket1"]==0:
                return "all out",5    
            if check[0]["input_1"]==0 or check[0]["input_2"]==0:
                return "waiting for your and your friend's input",0
            elif check[0]["input_1"]==check[0]["input_2"]:
                return "out",3
            elif check[0]["input_1"]!=check[0]["input_2"]:
                return "not out",4       
        elif check[0]["innings"]==2:
            #to check if target is set by other player and reached       
            if check[0]["run1"]!=0:
                if check[0]["run2"]==check[0]["run1"]:
                    return "match won by 2nd player",2
                elif check[0]["wicket2"]==0:
                    return "all out match won by 1st player",1
            elif check[0]["wicket2"]==0:
                return "all out",5
            if check[0]["input_1"]==0 or check[0]["input_2"]==0:
                return "waiting for your and your friend's input",0
            elif check[0]["input_1"]==check[0]["input_2"]:
                return "out",3
            elif check[0]["input_1"]!=check[0]["input_2"]:
                return "not out",4         
    except:
        return "unexpected err",400