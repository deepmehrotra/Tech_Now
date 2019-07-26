# Tech_Now
Documentation and general PDA 

Useful Links:

https://github.com/harvies/books/tree/master/Java/%5BJAVA%5D%5BEffective%20Java%203rd%20Edition%5D


package com.jpm.learn.threads;

import java.util.concurrent.*;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * Executor Interface :
 *   - executor extends Executor Interface
 *   -Executors gives factory method for creating executor service
 *
 *
 * #Waiting queue
 *  - Task are maintained in queue in executor
 *  - We cannot know if given task is executed or not
 *  - We can cancel a task submitted to executor if not picked up by any thread fro mwaiting queue.
 *  - We can pass instances of Runnable to executor
 *
 * # Runnable
 *  - Runnable cannot return anything
 *  - Runnable : No exceptions can be raised by runnable - e.g. if long running db query is there which is running in new thread then any error cannot be propagated
 *
 * # Callable interface
 *
 * #Diferent Excutors:
 * 1. SingleThreadExecutor
 * 2. FixedThreadPool
 * 3. Cashed Threadpool
 * 4. ScheduledThreadPool
 *
 *
 */
public class Sample {

    public static void main(String[] args) {
        Runnable task1=()-> System.out.println(" Thread name : "+Thread.currentThread().getName());
        ExecutorService executor= Executors.newSingleThreadExecutor();
        for(int i=0;i<10;i++){
            executor.submit(task1);
        }

    }

    public void lockPattern(){
        /**
         * Option 1 of making anything synchronous is using synchrounized key work
         * Drawback is : if any thread inside synchronized got stuck only way out is to restart JVM
         * To overcome that lock pattern comes
         * By default ReentrantLock is not fair in nature. So if two locks are waiting any object can take lock.
         * But if you put ReentrantLock(true) it keeps the fairness of the lock. First come first serve
         */
        Lock lock=new ReentrantLock();
        try{
            lock.lock();
            /**
             * lockInterruptibly will throw exception if any other thread tried and interrupt it during execution
             */
            lock.lockInterruptibly();

            //tryLock
            lock.tryLock();
        } catch (InterruptedException e) {
            e.printStackTrace();
        } finally {
            lock.unlock();
        }
    }
    /**
     * if executor service is not shutdown it keeps the jvm running . Because these are non dying threads.
     */
    public void executorShutdown(){
        Runnable task1=()-> System.out.println(" Thread name : "+Thread.currentThread().getName());
        ExecutorService executor= Executors.newSingleThreadExecutor();
        for(int i=0;i<10;i++){
            executor.submit(task1);
        }
        executor.shutdown();
    }

    /**
     * if executor service is not shutdown it keeps the jvm running . Because these are non dying threads.
     */
    public void executorServiceFixedThreadpool(){
        Runnable task1=()-> System.out.println(" Thread name : "+Thread.currentThread().getName());
        ExecutorService executor= Executors.newFixedThreadPool(4);
        for(int i=0;i<10;i++){
            executor.submit(task1);
        }
        executor.shutdown();
    }

    public void createExecutors() throws InterruptedException {
        //Creation using executors class
        //very used in reactive programming
        ExecutorService executor= Executors.newSingleThreadExecutor();

        //Fixed threadpool executor for creating executors for fixed number of threads
        //It takes number of threads as parameter
        //Number of threads depends on different parameters but for io intensives task make more threads but for computational intensive make threads equal to number of cores
        ExecutorService executorService=Executors.newFixedThreadPool(7);
        Runnable task1=()-> System.out.println(" Thread name : "+Thread.currentThread().getName());
        Runnable task2=()-> System.out.println(" Thread name : "+Thread.currentThread().getName());

        executorService.execute(task1);executorService.execute(task2);

        //Calable and Future
        Callable<Integer> intTask=()-> 5;
        Future<Integer> future= executorService.submit(intTask);
        try {
            /**
             *  Get methods will print the result if it is available
             But if it is not available then it will block the execution of main threads and then wait for result.
             It will throw InterruptedException - if the thread executing this task is interrupted e.g. shutdown onf executor service
             It will throw ExecutionException - if the task threw any exception
             If provided timeout it will throw TimeoutException exception
             Timeout to the get method to keep track of task
             */

            System.out.println(future.get());
            System.out.println(future.get(12,TimeUnit.SECONDS));
        } catch (InterruptedException e) {
            e.printStackTrace();
        } catch (ExecutionException e) {
            e.printStackTrace();
        } catch (TimeoutException e) {
            e.printStackTrace();
        }finally {
            /**
            * Manadatory
             * It will run all the task assigned to Threads and also complete all task in the queue
             * after shutdown it will not task any new task but finish task at work
             * This is soft shutdown.
             */
            executor.shutdown();

            /**
             * This will halt the runnign task
             * This will not run any waiting task and then shutdown
             */
            executor.shutdownNow();

            /**
             * It shutdown the executor
             * Then wait for some time for running task to complete and then kill all the task
             */
            executor.awaitTermination(10,TimeUnit.SECONDS );
        }


    }
}
================================================================
package com.jpm.learn.threads;

import java.util.LinkedList;
import java.util.List;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.Lock;
import java.util.concurrent.locks.ReentrantLock;

/**
 * #Condition interface: java.util.concurrent.locks package.
 * Condition instance are similar to using Wait(), notify() and notifyAll() methods on object.
 *
 * In case of traditional synchronization, there is only one object monitor so we can have only single wait-set per object. But,
   Condition instance are used with Lock instance, Condition factors out the Object monitor methods (wait, notify and notifyAll) into distinct objects to give the multiple wait-sets per object.

   Lock replaces the use of synchronized methods and blocks, & a Condition replaces the use of the Object monitor methods.

 *
 *  - Condition await() method is similar to object wait() method
 *  - method causes the current thread to wait until :
        signal()/signalAll() method is called, or
        current thread is interrupted.
 *
 * - Fair and Unfair Renetranct lock -
 *  if multiple threads are blocked then FIFO will applied for asigning job else longestwaiting thread
 *
 * - Await method takes Time to signal and after that it will return false condition.await(10,TimeUnits.Seconds)
 */
public class ProducerConsumer {
    /**
     * IllegalMonitorStateException is thrown if this lock is not held when any of the
     * Condition waiting or signalling methods are called.
     *
     */
    public void learnCondition(){
        Lock lock = new ReentrantLock();
        Condition producerCondition = lock.newCondition();

    }

    public static void main(String[] args) {
        List<Integer> sharedQueue = new LinkedList<Integer>(); //Creating shared object

        Lock lock = new ReentrantLock();
        //producerCondition - isFull condition
        Condition producerCondition = lock.newCondition();
        //consumerCondition - isEmpty condition
        Condition consumerCondition = lock.newCondition();

        Producer producer=new Producer(lock,sharedQueue,producerCondition,consumerCondition);
        Consumer consumer=new Consumer(lock,sharedQueue,producerCondition,consumerCondition);

        Thread producerThread = new Thread(producer, "ProducerThread");
        Thread consumerThread = new Thread(consumer, "ConsumerThread");
        producerThread.start();
        consumerThread.start();


    }
}

class Producer implements Runnable{

    List<Integer> sharedQ;
    Lock lock;
    Condition producerCondition;
    Condition consumerCondition;
    int maxSize=2;

    public Producer(Lock lock, List<Integer> sharedList, Condition producerCondition , Condition consumerCondition ){
        this.lock=lock;
        this.producerCondition=producerCondition;
        this.consumerCondition=consumerCondition;
        this.sharedQ=sharedList;
    }

    @Override
    public void run() {
        for (int i = 1; i <= 10; i++) {  //produce 10 products.
            try {
                produce(i);
            } catch (InterruptedException e) {  e.printStackTrace();   }
        }
    }

    public void produce(int i) throws InterruptedException {
        lock.lock();
        System.out.println(" Thread name : "+Thread.currentThread().getName());
        if(sharedQ.size()==maxSize){
            producerCondition.await();
        }

        System.out.println("Produced : "+i);
        sharedQ.add(i);
        consumerCondition.signal();
        lock.unlock();
    }
}

class Consumer implements Runnable{

    private Lock lock;
    List<Integer> sharedQ;
    Condition producerCondition;
    Condition consumerCondition;
    int maxSize=2;

    public Consumer(Lock lock, List<Integer> sharedList, Condition producerCondition , Condition consumerCondition ){
        this.lock=lock;
        this.producerCondition=producerCondition;
        this.consumerCondition=consumerCondition;
        this.sharedQ=sharedList;

    }

    @Override
    public void run() {
        for (int i = 1; i <= 10; i++) {  //produce 10 products.
            try {
                consume();
            } catch (InterruptedException e) {  e.printStackTrace();   }
        }
    }

    public void consume() throws InterruptedException {

        lock.lock();
        System.out.println(" Thread name : "+Thread.currentThread().getName());
        if(sharedQ.size()==0)
            consumerCondition.await();

        System.out.println(" Consumer : "+sharedQ.remove(0));

        producerCondition.signal();

        lock.unlock();
    }
}

