----------------------------------------------------------------------------------------------------------------
                                                Part - I
----------------------------------------------------------------------------------------------------------------

Filename = matrixMul.c
Binary   = matrixMul
Makefile = make -f makefile.matrix

# Sample output:
[user12@scc hw1]$ ./matrix -s 4096 -t 88
matrix size 4096, number of threads 88
elapsed time 11.088023 sec

# Implementation Details:
In order to reduce the running time of parallel execution I implemented the follwings steps

         * Assign random values only to upper traingle
         * copy the values from upper triangle to lower triangle
         * Included scheduled dynamic to improve the distribution of work since
           not each loop contains same amount of work . Loop iterations are dynamically
           assigned to threads
         * Added nowait to avoid barrier
         * Compute the output only for the upper triangle and copy the result to lower traingle

----------------------------------------------------------------------------------------------------------------
                                                Part - II
----------------------------------------------------------------------------------------------------------------

Filename = queuing.c
Binary   = queuing
Makefile = make -f makefile.queue

# Sample output 1
N=1000, L=3.0, M=4.0, N=1
Average customer Inter arrival time      = 0.330660
Standard Deviation Inter arrival time    = 0.337948
Average customer waiting time            = 0.510680
Standard Deviation customer waiting time = 0.707874
Average customer service time            = 0.245267
Standard Deviation customer service time = 0.233445
Average Queue length                     = 1.540000
Standard Deviation queue length          = 2.472747
Utilization time                         = 0.713677 sec

# Sample output 2
N=1000, L=3.0, M=4.0, N=3
Average customer Inter arrival time      = 0.331290
Standard Deviation Inter arrival time    = 0.332693
AAverage customer waiting time           = 0.001852
Standard Deviation customer waiting time = 0.015070
Average customer service time            = 0.250384
Standard Deviation customer service time = 0.243741
Average Queue length                     = 0.004000
Standard Deviation queue length          = 0.063119
Utilization time                         = 0.745216 sec

# Sample output 3
N=1000, L=3.0, M=4.0, N=5
Average customer Inter arrival time      = 0.334587
Standard Deviation Inter arrival time    = 0.335366
Average customer waiting time            = 0.000112
Standard Deviation customer waiting time = 0.000026
Average customer service time            = 0.249170
Standard Deviation customer service time = 0.238562
Average Queue length                     = 0.001000
Standard Deviation queue length          = 0.031607
Utilization time                         = 0.741236 sec

# Basic Setup:

        * By default Three threads are created
        * MUTEX VARAIBLES and CONDITION VARIABLEs are created for the pthreads
        * PTHREAD_CANCEL_ENABLED attribute is set to all the server threads
        * All the thread uses MUTEX lock and unlock to achieve thread synchronization
        * Thread 1 is programmed to send SIGNAL to thread 2 if everytime a new customer gets added to an empty queue
        * Thread 2 checks the queue and services the customer based on the number of servers specified
        * Thread 3 obtains the data from Thread 1 and Thread 2 and perform some statistics calculation
        * In the MAIN program the threads attribute is set to PTHREAD_CREATE_JOINABLE
        * Finally threads are joined together

# Thread functions:

        * Thread 1 and Thread 2 works on calculating the MEAN and SD for the Inter arrival, service and wait time
        * Thread 1 calculates the MEAN and SD for inter arrival time by drawing a Random distibution from generate_arrival_time() function
        * Thread 2 calculates the MEAN and SD for service time by drawing a Random distribution from generate_service_time() function
        * Thread 1 uses pthread_cond_broadcast() function to send signals to the server If the system has more than 1 server
        * Thread 2 maintain a THRESHOLD pointer to terminate all the server threads when 1000 customer are serviced

# Statistics:

        * Waiting time  = (customer service time) - (customer arrival time)
        * IAT           = customer arrival time with paramater lambda
        * Service time  = customer service time with paramter mu
        * Utilization   = service time / total elapsed time

# Problems encountered / Bug:

        * When using more than 1 server, occasionally Customer "x" is removed by server threads before customer "x" gets added into the queue which causes the system UNSTABLE
