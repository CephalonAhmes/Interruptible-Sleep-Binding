#include <pybind11/pybind11.h>
#include "../InternalLibrary/InterruptibleSleep.h"


PYBIND11_MODULE(InterruptibleSleepBinding, module)
{
    module.def("sleep_for_x_milliseconds", &sleep_for_x_milliseconds);
}
