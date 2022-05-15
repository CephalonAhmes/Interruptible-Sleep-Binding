cmake_minimum_required(VERSION 3.0.0)


project(InterruptibleSleepBinding)

include(CTest)
enable_testing()

add_subdirectory(pybind11)
add_subdirectory(src/InternalLibrary)

file(GLOB SOURCES CONFIGURE_DEPENDS "src/PythonBinding/*")
pybind11_add_module(PythonBinding ${SOURCES})
target_link_libraries(PythonBinding PUBLIC InternalLibrary)

file(GLOB SRC_FILES
    CONFIGURE_DEPENDS
	"tests/cpp_tests/*.cpp"
	"tests/cpp_tests/*.h"
)

add_executable(unit_tests ${SRC_FILES})
target_link_libraries(unit_tests PUBLIC InternalLibrary)
add_test(NAME Interruptible_Sleep_tests COMMAND unit_tests)
