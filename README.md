# plantower-PMS5003T-data-read
攀藤PMS5003T数据读取

使用树莓派读取攀藤设备

```python
if __name__ == '__main__':<br>
    test = plantower('/dev/ttyAMA0')<br>
    test.openSerial()<br>
    test.getDataStart()<br>
    print(test.dataAnalysis())<br>
```
