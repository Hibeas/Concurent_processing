#!/bin/bash
for i in {1..4}
do
(
echo "Process $i: Hello you";
sleep 5;
echo "Process $i: Bye bye!"
) &
done

