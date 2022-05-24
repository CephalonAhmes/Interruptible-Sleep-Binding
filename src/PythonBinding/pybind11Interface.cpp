#include <pybind11/pybind11.h>

#include "../InternalLibrary/InterruptibleSleep.h"

PYBIND11_MODULE(InterruptibleSleepBinding, module) {
    module.def("sleep_for_x_milliseconds", &sleep_for_x_milliseconds, "Sleeps for a certain amount of time. SIGINT and SIGTERM should interrupt the sleep and return to the python execution. The caught signal will be returned to the python side for you to handle.");
}
