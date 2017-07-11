def main():
    comma = 0
    s = ""
    out = open("a.csv", "w+")
    for line in open("AllanAcdAlt1.csv"):
        for c in line:
            if(c == "," and comma%2 == 0):
                s += "."
                comma += 1
            elif(c == ","):
                s += ","
                comma += 1
            else:
                s += c

        out.write(s)
        s = ""
        comma = 0
        
main()