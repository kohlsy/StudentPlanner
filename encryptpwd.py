def password(a):
    newpass=""
    for i in a:
            newpass=newpass+chr(ord(i)+4)

    print(newpass)
