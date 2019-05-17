import serial,time

s=serial.Serial('COM12',256000,timeout=1)
s.dtr=False
s.write(b'\xa5\xf0\x02\x94\x02\xc1')
time.sleep(5)
s.write(b'\xa5\x20')
time.sleep(1)
while True:
    d = s.read(5)
    #time.sleep(0.00001)
    print(d)
    print('\n')
s.write(b'\xa5\x25')
s.write(b'\xa5\xf0\x02\x00\x00\x57')