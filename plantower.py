#!/usr/bin/env python3
# -*- conding:uft-8 -*--
# @Author: dofospider
# @Date:   2018-09-11 09:29:50
# @Last Modified by:   dofospider
# @Last Modified time: 2018-09-13 22:39:13

'''

# This is a module for plantower senser serial data read
#
# This file suit for plantower senser PMS5003T
#
# Auther:dofospider
'''
import serial
import queue


class plantower(object):
    '''This is a class for plantower senser serial data read.

    '''

    def __init__(self, serial_driver,):
        '''Initialize seial port for communicate plantower senser.

        Arguments:
            serial_driver {str} -- [Need input a string.raspberry's like this '\\dev\\ttyAMA0']
            data_count{int} -- [The read of number types.default value is 80.You can change it when you need.]
            plantower_data{bytes} -- [Bytes from serial.]
        '''
        self.serial_driver = serial_driver
        self.data_count = 80
        self.plantower_data = b'BM\x00\x1c\x00#\x00+\x00,\x00\x1c\x00&\x00,\x16\xef\x06\xe4\x00\xa2\x00\x05\x01\x18\x01P\x91\x00\x05$BM\x00\x1c\x00#\x00+\x00,\x00\x1c\x00&\x00,\x16\xef\x06\xe4\x00\xa2\x00\x05\x01\x19\x01P\x91\x00\x05%BM\x00\x1c\x00#\x00+\x00,\x00\x1c\x00&\x00,'
        self.data_queue = queue.Queue()
        self.data_list = []
        self.count_total = 0

    def dataTotal(self, data_high, data_low):
        '''return the data high 8 bits *256 plus low 8 bits values.

        Arguments:
            data_high {int} -- [the number of high 8 bits]
            data_low {int} -- [the number of low 8 bits]

        Returns:
            [int] -- [the number of sum]
        '''
        return data_high * 256 + data_low

    def openSerial(self):
        ''' open serial bandrate=9600,timeout=1
            read date to plantower_data
        '''
        try:
            my_serial = serial.Serial(self.serial_driver, 9600, timeout=1)

            self.plantower_data = my_serial.read(self.data_count)
        except:
            print("serial port is fail")

    def getDataStart(self):
        '''from plantower_data get data to data_queue,then check the plantower magic_data.if the data is the plantower data then get the
        count_total.
        '''
        try:

            for i in self.plantower_data:
                self.data_queue.put(i)

            while(self.data_queue.qsize != 0):
                if(self.data_queue.get() == 66):
                    if(self.data_queue.get() == 77):

                        self.count_total = self.dataTotal(
                            self.data_queue.get(), self.data_queue.get())

                        break

                    else:
                        continue
                else:
                    continue

        except:
            print('plantower data is error')

    def dataAnalysis(self):
        '''Analysis the data in the data_queue,zip it in to the dict and return it.
        the dict key is ['pm1_cf1', 'pm25_cf1', 'pm10_cf1', 'pm1', 'pm25', 'pm10','pm0301', 'pm0501', 'pm1001', 'pm2501', 'temperature', 'humidity', ] you can change it suit your driver.
        '''
        try:

            data_check_end = 0
            data_check = 0
            count = self.count_total / 2
            data_check = data_check + 66 + 77 + self.count_total
            while(count > 0):
                count = count - 1
                data_high = self.data_queue.get()
                data_low = self.data_queue.get()
                data_check_end = data_high + data_low
                data_check = data_check + data_check_end
                self.data_list.append(self.dataTotal(
                    data_high, data_low))

            data_check = data_check - data_check_end

            data_key = ['pm1_cf1', 'pm25_cf1', 'pm10_cf1', 'pm1', 'pm25', 'pm10',
                        'pm0301', 'pm0501', 'pm1001', 'pm2501', 'temperature', 'humidity', ]

            if(data_check == self.data_list[-1]):
                return(dict(zip(data_key, self.data_list[:-2])))
            else:
                return(-1)
        except:
            print('Analysis data error')


if __name__ == '__main__':
    test = plantower('/dev/ttyAMA0')
    test.openSerial()
    test.getDataStart()
    print(test.dataAnalysis())
