# transit-app
Python app that determines the transit time between subway or public transportation stations


Please write the solution to the following exercise in python and include any relevant tests for your code.

Problem description:

Keep track of average transit times between stations in a subway or other public transportation system.

Each rider has a transit card, which they swipe in when entering a station AND swipe out when exiting a station. The cards have unique numbers, and we can assume that riders do not share or lose cards.

For example, someone enters 59th street station at 9:30:00 and exits 14th street station at 9:39:30, average is 570 seconds. If someone later makes the same trip, entering at 10:15:00 and exiting at 10:24:00, average drops to 555 seconds.

We wish to implement a program which saves entry/exit swipe information (card, time, station) and prints the average transit time for a given pair of stations.

Average transit times should be printed in seconds.

If there are no trips to calculate an average, just print -1.

Read input from STDIN. Print output to STDOUT.


Example inputs/outputs:

Input 1: \
Entry: card number: 1, station: A, time: 2021/05/01 09:30:00\
Output 1:\
Entry saved!\

Input 2:\
Exit: card number: 1, station: B, time: 2021/05/01 09:39:30\
Output 2:\
Entry saved!\

Input 3:\
Average A B\
Output 3:\
570 seconds\

Input 4:\
Entry: card number: 2, station: A, time: 2021/05/01 \
Output 4:\
Invalid entry time!\

Input 5:\
Entry: card number: abc, station: A, time: 2021/05/01 20:00.00\
Output 5:\
Invalid card number!\

Input 6:\
Entry: card number: 2, station: A, time: 2021/05/01 10:15:00\
Output 6:\
Entry saved!\

Input 7:\
Entry: card number: 2, station: B, time: 2021/05/01 10:24:00\
Output 7:\
Entry saved!\

Input 8:\
Average A B\
Output 8:\
555 seconds\

Input 9:\
Average A C\
Output 9:\
-1

Input 10:\
Entry: card number: 1, station: C, time: 2021/05/02 11:00:00\
Output 10:\
Entry saved!\

Input 11:\
Entry: card number: 1, station: A, time: 2021/05/02 11:05:00\
Output 11:\
Entry saved!\

Input 12:\
Average C A\
Output 12:\
300 seconds
