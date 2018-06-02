#include <stdio.h>
#include <stdlib.h>
#include <math.h>
/*#include <time.h>*/
#include <pthread.h>
#include<unistd.h>
#include<sys/time.h>
#define MAX 2000

struct customer {
        double ID;  /* Customer ID */
        double  tv1sec;
        double  tv2sec;
        double  tv1micro;
        double  tv2micro;
        double IAT;
        double WT;
        double ST;
        unsigned QL;
};

struct timeval tv1, tv2;
struct timeval ut1, ut2;
float sec;

struct customer queue_array[MAX];

int rea = - 1;
int fron = - 1;
int thresh = 1;
double ql = 0.0;
double st = 0.0;


int *rear = &rea;
int *front = &fron;
int *threshold = &thresh;

int count = 1;
int wake_up = 1;
int queue_l = 0;
int arr_count = 0;
int k = 0;
double *avg_QL = &ql;
double *avg_ST = &st;
double sD_QL;
unsigned no_server, size;
float new_cust, service_time;
double lambda, mu, avg_WT, avg_IAT, sD_WT, sD_ST, sD_IAT, UT, total_time;
int h, v, s, y, z;


pthread_mutex_t lockmutex;
pthread_cond_t full;
pthread_cond_t empty;
pthread_t threads[10];
struct drand48_data buffer;
/* rndExp generates pseudorandom numbers following the exponential
 *    distribution with parameter lambda*/
double rndExp(double lambda){
  double random_value;

  drand48_r(&buffer, &random_value);
  return -log(1.0 - random_value) / lambda;
}

/* mySleep shows how to sleep for nano sec*/
void Sleep_lambda(double rndSleep){
  struct timespec sleepTime;
    lambda = 3.0;
    rndSleep = rndExp(lambda);
    sleepTime.tv_sec = (unsigned)floor(rndSleep);
    sleepTime.tv_nsec = (rndSleep - sleepTime.tv_sec) * 1000000000L;
    nanosleep(&sleepTime, NULL);
  }

void Sleep_mu(double muSleep){
  struct timespec sleepTime;
    mu = 4.0;
    muSleep = rndExp(mu);
    sleepTime.tv_sec = (unsigned)floor(muSleep);
    sleepTime.tv_nsec = (muSleep - sleepTime.tv_sec) * 1000000000L;
    nanosleep(&sleepTime, NULL);
  }

double generate_arrival_time(){
        return  rndExp(lambda);
}

double generate_service_time(){
        return rndExp(mu);
}

int wasEmpty(){
        int check = *front - *rear;;
        if(check == 0){ return 0; }
        else { return 1; }
}

struct timespec sleepTime;
/* This thread is responsible for generating the customers */
void *thread_one(void *t1) {
pthread_mutex_lock( &lockmutex);
while(wake_up) {
        new_cust = generate_arrival_time();
        Sleep_lambda(new_cust);
        if(*front == -1) { *front = 0; };
        ++*rear;
        printf("Thread %ld == Adding customer %d in queue\n", t1, *rear);
        printf("Length of the queue = %d\n", *rear-*front+1);
        gettimeofday(&tv1, NULL);
        queue_array[*rear].tv1sec = tv1.tv_sec;
        queue_array[*rear].tv1micro = tv1.tv_usec;
        queue_array[*rear].IAT = new_cust;
        avg_IAT = queue_array[*rear].IAT + avg_IAT;
        if (wasEmpty() == 0) {
                /* Thread 1 signals to Thread 2 */
                printf("Signal sent to calling thread Adding customer %d\n", *rear);
                pthread_cond_broadcast( &empty);
                }
   pthread_mutex_unlock( &lockmutex);
  }
    pthread_exit(NULL);
}



int  var[] = {10, 100, 200};
/* This thread is responsible for serving the customers */
void *thread_two(void *t2) {
pthread_mutex_lock( &lockmutex);
gettimeofday(&ut1, NULL);
pthread_setcancelstate(PTHREAD_CANCEL_ENABLE, NULL);
int i, *some[3];
while(*threshold){
    printf("Front = %d and size = %d  and rear = %d and Threshold = %d\n", *front, size, *rear, *threshold);
    if(*front == size) {some[0]=&var[0]; *threshold = 0;}
    if(*front > *rear) {
        printf("No customer in queue , waiting for signal from Thread 1\n");
        pthread_cond_wait( &empty, &lockmutex);
        printf("Conditional signal Received\n");
        pthread_mutex_unlock( &lockmutex);
     }
    else {
        gettimeofday(&tv2, NULL);
        ++*front;
        printf("Thread %ld == Removing Customer %d from queue\n", t2, *front-1);
        queue_array[*front-1].tv2sec = tv2.tv_sec;
        queue_array[*front-1].tv2micro = tv2.tv_usec;
        /*printf("Arrival time in sec and micro = %f sec %f micro\n", queue_array[front].tv2sec, queue_array[front].tv2micro);
        printf("Departure time in sec and micro = %f sec %f micro\n", queue_array[front].tv2sec, queue_array[front].tv2micro);*/
        queue_array[*front-1].WT = (queue_array[*front-1].tv2sec - queue_array[*front-1].tv1sec) + (queue_array[*front-1].tv2micro - queue_array[*front-1].tv1micro) / 1000000.0;
        printf("Customer %d waiting time is = %f\n", *front-1, queue_array[*front-1].WT);
        avg_WT = queue_array[*front-1].WT + avg_WT;

        /* Queue length statistics*/
        queue_l = *rear-*front+1;
        queue_array[*front-1].QL = queue_l;
        *avg_QL = queue_array[*front-1].QL + *avg_QL;
        printf("The total queue length from 2 threads = %f\n", *avg_QL);

        /* Service time statistics*/
        service_time = generate_service_time();
        Sleep_mu(service_time);
        queue_array[*front-1].ST = service_time;
        *avg_ST = queue_array[*front -1].ST + *avg_ST;

        pthread_mutex_unlock( &lockmutex);
    }
  }
        /* End of While loop*/
        gettimeofday(&ut2, NULL);
        printf("Total no of threads = %d\n", no_server+2);
        printf("Thread ID  = %ld\n", (long)t2);
        if(*some[0] == var[0]){
        printf("Some = %d\n", *some[0]);
        printf("Thread 0 Terminated\n");
        pthread_cancel(threads[0]);

        printf("Thread %d Terminated\n", no_server+1);
        pthread_cancel(threads[no_server+1]);

        printf("Thread %ld Terminated\n", (long)t2);
        pthread_cancel(threads[(long)t2]);

        for(v=0; v<size; v++){ sD_WT += pow(queue_array[v].WT - (avg_WT/size), 2); }
        for(s=0; s<size; s++){ sD_ST += pow(queue_array[s].ST - (*avg_ST/size), 2); }
        for(y=0; y<size; y++){ sD_IAT += pow(queue_array[y].IAT - (avg_IAT/size), 2); }
        for(z=0; z<size; z++){ sD_QL += pow(queue_array[z].QL - (*avg_QL/size), 2); }
        some[0] = &var[1];
        }

        else {
                printf("Some = %d\n", *some[0]);
                printf("Thread %ld Terminated\n", (long)t2);
                pthread_cancel(threads[(long)t2]);
        }

        pthread_exit(NULL);

}


/* This thread is responsible for collecting the statistics data */
void *thread_three(void *t3) {

pthread_mutex_lock( &lockmutex);
while(1) {
        sleep(0.01);
        UT = (queue_l * mu) + UT;
        arr_count++;
        pthread_mutex_unlock( &lockmutex);
  }

        pthread_exit(NULL);
}


int main(int argc, char *argv[]) {
int c, p;
unsigned i, k;
long t1=0, t2=1, t3=2;
pthread_attr_t attr;

 while ((c = getopt(argc, argv, "C:L:M:N:")) != -1){
    switch (c){
    case 'C': sscanf(optarg, "%u", &size); break;
    case 'L': sscanf(optarg, "%lf", &lambda); break;
    case 'M': sscanf(optarg, "%lf", &mu); break;
    case 'N': sscanf(optarg, "%u", &no_server); break;
    default: break;
    }
  }

if(no_server == 0){no_server = 1;}
if(lambda >= mu*no_server){printf("System is Unstable\n"); exit(0);}
if(no_server > 5){printf("No of server should be between 1 and 5\n"); exit(0);}

/* Initialize mutex and condition variable objects */
pthread_mutex_init( &lockmutex, NULL);
pthread_cond_init ( &empty, NULL);

/* For portability, explicitly create threads in a joinable state */
        pthread_attr_init(&attr);
        pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
        printf("Thread %ld created\n", t1);
        pthread_create(&threads[0], &attr, thread_one, (void *)t1);
        if(no_server == 1){
                        printf("Thread %d created\n", no_server);
                        pthread_create(&threads[1], &attr, thread_two, (void *)t2);
                        }
        else{
                for(p = 1; p <= no_server; p++){
                        printf("Thread %d created\n", p);
                        pthread_create(&threads[p], &attr, thread_two, (void *)p);
                }
            }
        printf("Thread %d created\n", no_server+1);
        pthread_create(&threads[no_server+1], &attr, thread_three, (void *)no_server+1);

        for (i=0; i<=(no_server+1); i++) {
        pthread_join(threads[i], NULL);
        }

        printf("\n");
        printf("----------------------STATISTICS--------------------------\n");
        printf("\n");
        printf("Average customer Inter arrival time = %f\n", avg_IAT/size);
        printf("Standard Deviation Inter arrival time = %f\n", sqrt(sD_IAT/size));
        printf("\n");
        printf("Average customer waiting time = %f\n", avg_WT/size);
        printf("Standard Deviation customer waiting time = %f\n", sqrt(sD_WT/size));
        printf("\n");
        printf("Average customer service time = %f\n", *avg_ST/size);
        printf("Standard Deviation customer service time = %f\n", sqrt(sD_ST/size));
        printf("\n");
/*      printf("Queue length is %f and size is %d\n", avg_QL, size);*/
        printf("Average Queue length = %f\n", *avg_QL/size);
        printf("Standard Deviation queue length = %f\n", sqrt(sD_QL/size));
        printf("\n");
        total_time = (ut2.tv_sec-ut1.tv_sec) + (ut2.tv_usec-ut1.tv_usec) / 1000000.0;
        printf("Utilization time %f sec\n", *avg_ST/total_time);
        printf("\n");
        /*printf("Elapsed time %f sec\n", total_time);*/

/* Clean up and exit */
pthread_attr_destroy(&attr);
pthread_mutex_destroy(&lockmutex);
pthread_cond_destroy(&empty);
pthread_exit(NULL);
return 0;
}
