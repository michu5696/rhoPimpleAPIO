#ifndef APIO_H
#define APIO_H

#include <iostream>
#include <queue>
#include <string>
#include <condition_variable>
#include <mutex>
#include <thread>
#include <atomic>
#include <vector>

#include <mpi.h>

std::mutex mtx1,mtx2;
//double starttime,endtime;

//double non_overlapped_io_time=0;
double startio,endio;
double iotime=0;
double alliotime;

struct field_handler
{
   word f;
   std::string state;
   std::condition_variable cv;
   field_handler(const char * field) : state("WRITE_FINISHED"),f(word(field)){}
};




void writeFromQueue(int rank, std::atomic<bool>& running,std::queue<field_handler*>& queue,std::condition_variable& cv_worker, objectRegistry& mesh)
{
    std::cout << "writeThread "<< rank << " on CPU "<< sched_getcpu() << std::endl;
    while(running)
    {
        if(!queue.empty())
        {
            field_handler* field = queue.front(); 
	    queue.pop();
	    field->state="WRITING";
	    std::lock_guard<std::mutex> lck(mtx2); 
	    startio=MPI_Wtime();
	    mesh.getObjectPtr<regIOobject>(field->f,false)->write();
	    endio=MPI_Wtime();
	    iotime+=endio-startio;
	    //Info << "APIO_IO_STEP = "<< end-start <<endl;
	    field->state="WRITE_FINISHED";
	    field->cv.notify_one();
        }
        else
        {
    	    std::unique_lock<std::mutex> lck(mtx1);
            cv_worker.wait(lck,[&]{return !queue.empty()||!running;});
        }
    }

}

void Iwrite(std::vector<field_handler*> list, std::condition_variable& cv_worker, std::queue<field_handler*>& queue){
    //starttime=MPI_Wtime();
    for (field_handler* f : list)
    {
        f->state="WAIT_WRITE";
        std::lock_guard<std::mutex> lck(mtx1);
        queue.push(f);
        cv_worker.notify_one();
    }
    //endtime=MPI_Wtime();
    //non_overlapped_io_time+=endtime-starttime;
}

void Iwait(std::vector<field_handler*> list)
{
    //starttime=MPI_Wtime();
    for (field_handler* f : list)
    {
        std::unique_lock<std::mutex> lck(mtx2);
        f->cv.wait(lck,[&]{return f->state=="WRITE_FINISHED";});
    }
    //endtime=MPI_Wtime();
    //non_overlapped_io_time+=endtime-starttime;
}

#endif
