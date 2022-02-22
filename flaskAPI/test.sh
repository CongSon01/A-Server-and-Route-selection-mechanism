#!/bin/bash

sleep 10 & 
T1=${!}
sleep 600 & 
T2=${!}
sleep 1200 & 
T3=${!}
sleep 1800 & 
T4=${!}
sleep 3600 &
T5=${!}

echo "This script started 5 background threads which are currently executing with PID's ${T1}, ${T2}, ${T3}, ${T4}, ${T5}."
wait ${T1}
echo "Thread 1 (sleep 10) with PID ${T1} has finished!"
wait ${T2}
echo "Thread 2 (sleep 600) with PID ${T2} has finished!"