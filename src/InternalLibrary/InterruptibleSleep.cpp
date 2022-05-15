#include <thread>
#include <chrono>
#include <csignal>
#include <condition_variable>
#include "InterruptibleSleep.h"

std::condition_variable cv;
std::atomic<bool> signal_caught;

void signal_handler(int signal){
    cv.notify_all();
    signal_caught = true;
}

int sleep_for_x_milliseconds(int milliseconds_to_sleep_for)
{
    signal_caught = false;
    _crt_signal_t old_sig_int_handler = signal(SIGINT, signal_handler);

    std::mutex m;
    std::unique_lock<std::mutex> lock(m);
    cv.wait_for(lock, std::chrono::milliseconds(milliseconds_to_sleep_for));
    std::signal(SIGINT, old_sig_int_handler);

    if(signal_caught){
        return SIGINT;
    }

    return -1;
}