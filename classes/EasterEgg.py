import random
class EasterEgg(object):
    @staticmethod
    def getSantino():
        r = random.randint(0, 20)
        if (r >= 0 and r <= 3):
            output = "@Santinol"
        elif (r > 3 and r < 10):
            output = "https://s18.postimg.org/t13s9lai1/photo_2016_11_24_11_04_42.jpg"
        elif (r >= 10 and r < 16):
            output = "https://s11.postimg.org/yiwugh4ib/photo_2016_11_24_11_04_31.jpg"
        elif (r >= 16 and r < 21):
            output = "https://s12.postimg.org/5d7y88pj1/photo_2016_11_24_11_04_29.jpg"
        return output

    @staticmethod
    def getSmontaPortoni():
        r = random.randint(0, 13)
        if (r >= 0 and r <= 3):
            output = "$ sudo umount portoni"
        elif (r > 3 and r < 10):
            output = "@TkdAlex"
        elif (r == 11):
            output = "https://s16.postimg.org/5a6khjb5h/smonta_portoni.jpg"
        else:
            output = "https://s16.postimg.org/rz8117y9x/idraulico.jpg"
        return output

    @staticmethod
    def getBladrim():
        output = "Per maggiori informazioni contatta @bladrim"
        return output

