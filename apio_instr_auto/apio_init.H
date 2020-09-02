field_handler f_rho("rho"),f_rho_0("rho_0"), f_k("k"),f_k_0("k_0"), f_p("p"),f_p_0("p_0"),f_phi("phi"),f_phi_0("phi_0"), f_U("U"),f_U_0("U_0"),f_T("T"),f_nut("nut"),f_alphat("alphat");

std::queue<field_handler*> queue;
std::condition_variable cv_worker;
std::atomic<bool> running {true};

int rank = Pstream::myProcNo();
int nprocs = Pstream::nProcs();

// WRITER THREAD
std::thread writer (writeFromQueue,rank,std::ref(running),std::ref(queue),std::ref(cv_worker),std::ref(mesh));


// CPU PINNING
cpu_set_t cpuset;
CPU_ZERO(&cpuset);
CPU_SET(nprocs + rank, &cpuset);
pthread_setaffinity_np(writer.native_handle(),sizeof(cpu_set_t), &cpuset);

