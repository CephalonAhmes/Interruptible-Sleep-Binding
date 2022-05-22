#include <thread>
#include <chrono>
#include <csignal>
#include <system_error>
#include <condition_variable>
#include <atomic>
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
    auto old_sig_int_handler = std::signal(SIGINT, signal_handler);
    if ( old_sig_int_handler == SIG_ERR ) {
        throw std::runtime_error("Failed to set internal signal handler");
    }

    std::mutex m;
    std::unique_lock<std::mutex> lock(m);
    cv.wait_for(lock, std::chrono::milliseconds(milliseconds_to_sleep_for));
    auto response = std::signal(SIGINT, old_sig_int_handler);
    if ( response == SIG_ERR ) {
        throw std::runtime_error("Failed to reset to initial signal handler");
    }

    if(signal_caught){
        return SIGINT;
    }

    return -1;
}