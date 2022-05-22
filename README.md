# Interruptible-Sleep-Binding


## About
Interruptible-Sleep-Binding is a single-function python library written in C++ built specifically for another project of mine, where time.sleep()'s behavior was causing some issues related to signal handling.

When a python program is currently sleeping for a long time, not only can it not be interrupted through normal means (you'll have to wait all of those 60 seconds for you CRTL-C to get through. GRRR!), but all signal handlers stop responding until the end of the sleep. In small scripts, that shouldn't cause too many issues, but in my case immediate shutdown upon SIGINT was essential, as the platform I use sends a SIGKILL after a couple seconds unresponsive, and I needed to run some cleanup actions to commits information as needed.

Now, you'll tell me that doing some ugly hack like 
```
for i in range(60):
	time.sleep(1)
```
would do the trick. Well... Sorta, but I hate it. So I made a custom replacement in C++

## Usage

To install, just `pip install InterruptibleSleepBinding`. I've compiled a few wheels to make the module easier to install, but if you need to install from sdist, you will need to have cmake installed.

Here's an example of using the module:
```
import InterruptibleSleepBinding

response = InterruptibleSleepBinding.sleep_for_x_milliseconds(55)
```