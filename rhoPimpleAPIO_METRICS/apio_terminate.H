running=false;
cv_worker.notify_one();
writer.join();

//Info << "APIO_IO_TIME = " << io_time << endl;
//Info << "NON_OVERLAPPED_IO_TIME = " << non_overlapped_io_time << endl;
//Info << "APIO_EXECUTION_TIME = " << exectime <<endl;
