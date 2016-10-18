# zcutils
Python utils for Zcash. Currently implements a mining rate calculator.

## Prerequisites
A working Zcash daemon and Zcash build environment. See https://github.com/zcash/zcash/wiki/Beta-Guide.

Additional python libraries installed with
```
$ sudo apt-get python-matplotlib python-prettytable python-scipy
```

## Installing and running
Fetch the repository and change file mode
```
$ git clone https://github.com/JanKalin/zcutils.git
$ chmod +x zcutils/miningrate.py
```

When executed, the script will check the latest 10000 transactions (by default) for mined TAZ and generate some statistics.
It is also possible to generate a graph of mining data. Run `zcutils/miningrate.py -h` for help.

An example of running the script with default parameters:
```
jank@ubuntu-modeli:~$ zcutils/miningrate.py
Getting transactions ... 100%
Reading 16 blocks ... 100%
+--------+---------------------+----------+---------+----------+
| height |         time        | immature | dheight |  dtime   |
+--------+---------------------+----------+---------+----------+
|  4444  | 2016-10-12 18:03:13 |          |         |          |
|  4486  | 2016-10-12 19:38:22 |          |    42   | 1:35:09  |
|  4525  | 2016-10-12 21:29:28 |          |    39   | 1:51:06  |
|  4864  | 2016-10-13 11:43:12 |          |   339   | 14:13:44 |
|  4867  | 2016-10-13 11:46:41 |          |    3    | 0:03:29  |
|  4907  | 2016-10-13 13:36:27 |          |    40   | 1:49:46  |
|  4952  | 2016-10-13 15:26:08 |          |    45   | 1:49:41  |
|  5002  | 2016-10-13 17:33:12 |          |    50   | 2:07:04  |
|  5026  | 2016-10-13 18:44:12 |          |    24   | 1:11:00  |
|  5175  | 2016-10-14 00:04:17 |          |   149   | 5:20:05  |
|  5355  | 2016-10-14 08:16:10 |          |   180   | 8:11:53  |
|  5369  | 2016-10-14 08:47:21 |          |    14   | 0:31:11  |
|  5384  | 2016-10-14 09:19:07 |          |    15   | 0:31:46  |
|  5437  | 2016-10-14 11:16:54 |          |    53   | 1:57:47  |
|  5564  | 2016-10-14 17:00:59 |          |   127   | 5:44:05  |
|  5642  | 2016-10-14 19:56:37 |    *     |    78   | 2:55:38  |
+--------+---------------------+----------+---------+----------+
+------------+----------+---------+---------+
|        qty |   mean   |   std   |  median |
+------------+----------+---------+---------+
|    dheight | 79.8667  | 85.3541 | 45.0000 |
| blockttime | 0:02:23  | 0:00:25 | 0:02:26 |
|      dtime | 3:19:34  | 3:37:12 | 1:51:06 |
|     blocks |  15 + 1  |         |         |
| blocks/day |  7.4528  |         |         |
+------------+----------+---------+---------+
+---------------------+---------------+-------+
|         day         |  dtime [min]  | count |
+---------------------+---------------+-------+
| 2016-10-12 02:00:00 |     68.75     |  3.0  |
| 2016-10-13 02:00:00 | 227.830952381 |  7.0  |
| 2016-10-14 02:00:00 | 198.722222222 |  6.0  |
+---------------------+---------------+-------+
```

# Known issues
The timestamps are not calculated correctly, but for general idea of the mining rate it's good enough.
