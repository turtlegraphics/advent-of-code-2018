def fade(s,f):
    """Return a new string with str faded by ANSI color codes.
       fade = 0 is nearly white, 200 is black"""
    code = str(255-int(f*23.9/200.0))
    return u"\u001b[38;5;" + code + "m" + s + u"\u001b[0m"

if __name__=='__main__':    
    for f in range(200,-1,-1):
        print fade(str(f),f)
    
