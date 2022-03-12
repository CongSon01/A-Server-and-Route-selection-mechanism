#/bin/bash
 
# Usage: ./random_iperf_traffic.sh &amp;lt;hostname/IP&amp;gt; &amp;lt;time length&amp;gt;
# Outputs to filename &quot;random_traffic_iperf_date_time&amp;gt;
 
#Read in the command line params: time and target
 
host=$1
 
totalTime=$2
 
# Get the current date for the filename
fileDate=`date +%m_%d_%y_%T`
touch random_traffic_iperf_&quot;$fileDate&quot;.csv
 
# Now I need to run the iperf loop. The trick here is to stay within the time limit.
# For now, I'm going to take the target time ($time), and divide it in half before the loop. I'll start with a random
# length of time within that time contraint divided by 4, then work up to the $totalTime from there. This way, I ensure we'll have
# at least some random traffic generated.
 
splitTime=$(( totalTime / 4 ))
 
# Get a random time between the new time
time=`shuf -i 1-$splitTime -n 1`
 
while [ $totalTime -ne 0 ]
do
 
# nerfing this var due to the Pi limits of about 40Mbps
targetBandwidth=`shuf -i 1-40 -n 1`
 
# Output the current time and bandwidth target
echo `date +%D_%T`,&quot;$targetBandwidth&quot;Mbps &amp;gt;&amp;gt; random_traffic_iperf_&quot;$fileDate&quot;.csv 
 
echo Running iperf3 in client mode towards host $host at target bandwidth of &quot;$targetBandwidth&quot;Mbps for $time seconds.  
 
iperf3 -c $host -t $time -u -b &quot;$targetBandwidth&quot;m
 
totalTime=$((totalTime - time))
 
time=`shuf -i 1-$totalTime -n 1`
 
done