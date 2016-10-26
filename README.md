# zcutils
Python utils for Zcash. Currently implements a mining rate calculator.

## Prerequisites
A working Zcash daemon and Zcash build environment. See https://github.com/zcash/zcash/wiki/Beta-Guide.

Additional Python libraries, installed with
```
$ sudo apt-get python-matplotlib python-prettytable python-scipy
```

## Installing 
Fetch the repository
```
$ git clone https://github.com/JanKalin/zcutils.git
```

## Running `miningrate.py`

When executed, the script will check the latest 10000 transactions (by default)
for mined TAZ/ZEC and generate some statistics.  It is also possible to
generate a graph of mining data. Run `zcutils/miningrate.py -h` for help.

An example of running the script with the default parameters:
```
$ zcutils/miningrate.py
Getting transactions ... 100%
Reading 25 blocks ... 100%
+--------+---------------------+------------+----------+---------+---------+
| height |         time        | difficulty | immature | dheight |  dtime  |
+--------+---------------------+------------+----------+---------+---------+
|  8510  | 2016-10-19 16:50:29 |    491.81  |          |         |         |
|  8537  | 2016-10-19 17:46:35 |    546.90  |          |      27 | 0:56:06 |
|  8557  | 2016-10-19 19:02:59 |    444.78  |          |      20 | 1:16:24 |
|  8575  | 2016-10-19 19:47:23 |    456.63  |          |      18 | 0:44:24 |
|  8585  | 2016-10-19 20:01:54 |    455.31  |          |      10 | 0:14:31 |
|  8622  | 2016-10-19 21:48:46 |    400.89  |          |      37 | 1:46:52 |
|  8628  | 2016-10-19 22:04:53 |    396.31  |          |       6 | 0:16:07 |
|  8638  | 2016-10-19 22:46:36 |    395.69  |          |      10 | 0:41:43 |
|  8675  | 2016-10-20 00:08:50 |    382.98  |          |      37 | 1:22:14 |
|  8677  | 2016-10-20 00:12:17 |    397.09  |          |       2 | 0:03:27 |
|  8685  | 2016-10-20 00:20:17 |    399.57  |          |       8 | 0:08:00 |
|  8709  | 2016-10-20 01:17:56 |    442.77  |          |      24 | 0:57:39 |
|  8720  | 2016-10-20 01:45:45 |    454.53  |          |      11 | 0:27:49 |
|  8726  | 2016-10-20 01:58:59 |    463.60  |          |       6 | 0:13:14 |
|  8728  | 2016-10-20 02:00:05 |    474.48  |          |       2 | 0:01:06 |
|  8752  | 2016-10-20 02:47:51 |    608.63  |          |      24 | 0:47:46 |
|  8755  | 2016-10-20 02:57:02 |    618.93  |          |       3 | 0:09:11 |
|  8781  | 2016-10-20 04:24:17 |    534.21  |          |      26 | 1:27:15 |
|  8787  | 2016-10-20 04:32:54 |    463.24  |          |       6 | 0:08:37 |
|  8818  | 2016-10-20 06:24:14 |    366.40  |          |      31 | 1:51:20 |
|  8837  | 2016-10-20 07:10:40 |    313.59  |          |      19 | 0:46:26 |
|  8842  | 2016-10-20 07:19:51 |    324.39  |          |       5 | 0:09:11 |
|  8850  | 2016-10-20 07:29:38 |    343.87  |    *     |       8 | 0:09:47 |
|  8879  | 2016-10-20 08:25:22 |    475.41  |    *     |      29 | 0:55:44 |
|  8883  | 2016-10-20 08:39:32 |    482.37  |    *     |       4 | 0:14:10 |
+--------+---------------------+------------+----------+---------+---------+
+------------+---------+---------+---------+
|        qty |   mean  |   std   |  median |
+------------+---------+---------+---------+
| difficulty |  443.44 |   77.11 |  449.66 |
|    dheight |   15.54 |   11.18 |   10.50 |
| blockttime | 0:02:21 | 0:00:54 | 0:02:18 |
|      dtime | 0:39:33 | 0:33:05 | 0:34:46 |
|     blocks |  22 + 3 |         |         |
| blocks/day |   38.70 |         |         |
+------------+---------+---------+---------+
+------------+---------+-------+
|    day     |  dtime  | count |
+------------+---------+-------+
| 2016-10-19 | 0:44:31 |     8 |
| 2016-10-20 | 0:34:53 |    17 |
+------------+---------+-------+
```

### Known issues

Graphs are not well-documented and formatted

## Running `minerlist.py`

When executed the script will read the blockchain for information about
miners and print out a table. In order to speed up subsequent runs, a file
in temporary directory is used to cache data from previous runs.  Run
`minerlist.py -h` for help. 

An example of running the script is:
```
$ ./minerlist.py  @map.txt --last 1 --top 10
2322 blocks in cache
Reading blocks 2323 to at least 2323: 2323
Keeping last 603 blocks
+--------+-----------+-----------+-----------+-------------------------------------+
| blocks |   % bl.   |   value   |   % val.  |             name/address            |
+--------+-----------+-----------+-----------+-------------------------------------+
|    313 |   51.9071 |  317.6730 |   52.6821 |             suprnova.cc             |
|     34 |    5.6385 |   34.5896 |    5.7363 | tmCGbGuXcHs6dEhWwCKL9USwAqnQ8MzzjxU |
|     24 |    3.9801 |   24.0004 |    3.9802 |             coinmine.pl             |
|     23 |    3.8143 |   22.9355 |    3.8036 |             flypool.org             |
|      6 |    0.9950 |    5.7588 |    0.9550 | tmAY8sBmArJGMs9FTFPVH9yywLj1tUnSP1h |
|      5 |    0.8292 |    5.1589 |    0.8555 |               zmine.io              |
|      4 |    0.6633 |    3.3472 |    0.5551 | tmTXNiSh8rzVp9ZtF5eS5U7A2TpK6ScEc5W |
|      3 |    0.4975 |    0.7779 |    0.1290 | tmArktme2ryF45ynBT3LvciafbgPbD3EFqg |
|      2 |    0.3317 |    2.0580 |    0.3413 | tmYjw1tQfEYKzoR6spPodu3EmzyXBBsLTA9 |
|      1 |    0.1658 |    1.1610 |    0.1925 | tmDacMeLppwMMW7YDmVqKw2xzSNkz8Uvj8S |
+--------+-----------+-----------+-----------+-------------------------------------+
```

The file `map.txt` contains a mapping of address to pool name. This mapping
will have to be changed once the main net is online.
