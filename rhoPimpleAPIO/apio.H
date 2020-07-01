#ifndef APIO_H
#define APIO_H

#include <queue>
#include <string>
#include <condition_variable>
#include <mutex>
#include <thread>
#include <atomic>
#include <vector>

std::mutex mtx1,mtx2;


struct field_handler
{
   word f;
   std::string state;
   std::condition_variable cv;
   field_handler(const char * field) : state("WRITE_FINISHED"),f(word(field)){}
};




void writeFromQueue(std::atomic<bool>& running,std::queue<field_handler*>& queue,std::condition_variable& cv_worker, objectRegistry& mesh)
{
    while(running)
    {
        if(!queue.empty())
        {
            field_handler* field = queue.front(); 
	    queue.pop();
	    field->state="WRITING";
	    std::lock_guard<std::mutex> lck(mtx2); 
	    mesh.getObjectPtr<regIOobject>(field->f,false)->write();
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
    for (field_handler* f : list)
    {
        f->state="WAIT_WRITE";
        std::lock_guard<std::mutex> lck(mtx1);
        queue.push(f);
        cv_worker.notify_one();
    }
}

void Iwait(std::vector<field_handler*> list)
{
    for (field_handler* f : list)
    {
        std::unique_lock<std::mutex> lck(mtx2);
        f->cv.wait(lck,[&]{return f->state=="WRITE_FINISHED";});
    }
}

#endif
