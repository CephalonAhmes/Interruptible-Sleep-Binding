#include <csignal>
#include "../../src/InternalLibrary/InterruptibleSleep.h"
#include <chrono>
#include <iostream>
#include <thread>

#define CATCH_CONFIG_MAIN
#include "catch.hpp"

TEST_CASE("sleep for x milliseconds", "[classic]")
{
   SECTION("Test return value without signal")
   {
      REQUIRE(sleep_for_x_milliseconds(0) == -1);
   }

   SECTION("Test sleep duration is correct")
   {
      auto t1 = std::chrono::high_resolution_clock::now();
      sleep_for_x_milliseconds(10);
      auto t2 = std::chrono::high_resolution_clock::now();
      REQUIRE(std::chrono::duration_cast<std::chrono::milliseconds>(t2 - t1) >= std::chrono::milliseconds(10));
   }
}