import pyinsim

def message_out(insim, packet):
    pass

insim = pyinsim.insim('127.0.0.1', 29999)

insim.bind(pyinsim.ISP_MSO, message_out)

if __name__ == '__main__':
    pyinsim.run()
