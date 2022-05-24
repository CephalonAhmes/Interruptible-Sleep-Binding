#include "InterruptibleSleep.h"

#include <atomic>
#include <chrono>
#include <condition_variable>
#include <csignal>
#include <system_error>
#include <unordered_map>
#include <vector>

std::condition_variable cv;
std::atomic<int> caugth_signal;

void signal_handler(int signal) {
    cv.notify_all();
    caugth_signal = signal;
}

typedef void (*_old_signal_hanlder_type)(int);

int sleep_for_x_milliseconds(int milliseconds_to_sleep_for) {
    caugth_signal = -1;
    std::mutex m;
    std::unique_lock<std::mutex> lock(m);
    std::vector<int> signals_to_handle = {SIGINT, SIGTERM};
    std::unordered_map<int, _old_signal_hanlder_type> old_signal_handlers = {};

    for (int signal : signals_to_handle) {
        old_signal_handlers[signal] = std::signal(signal, signal_handler);
        if (old_signal_handlers[signal] == SIG_ERR) {
            throw std::runtime_error("Failed to set internal signal handler");
        }
    }

    cv.wait_for(lock, std::chrono::milliseconds(milliseconds_to_sleep_for));

    for (std::pair<int, _old_signal_hanlder_type> element : old_signal_handlers) {
        _old_signal_hanlder_type response = std::signal(element.first, element.second);
        if (response == SIG_ERR) {
            throw std::runtime_error(
                "Failed to reset to initial signal handler");
        }
    }

    return caugth_signal;
}