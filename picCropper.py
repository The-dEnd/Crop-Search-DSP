def cropToSquare(h, l):
    if h>l:
        return((h-l)/2,0,(h+l)/2,l)
    else:
        return(0,(l-h)/2,h,(l+h)/2)