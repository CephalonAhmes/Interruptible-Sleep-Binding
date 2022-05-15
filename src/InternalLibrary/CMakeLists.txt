file(GLOB SRC_FILES
    CONFIGURE_DEPENDS
	"*.cpp"
	"*.h"
)

add_library(InternalLibrary ${SRC_FILES})