CXX      = clang++ 
# CXXFLAGS = -std=c++17 -Wall -Wextra -pedantic		# za debug
CXXFLAGS = -std=c++17 -O3							# za testiranje
TARGET   = main.out

$(TARGET): main.cpp amts.cpp GraphClass.cpp GraphClass.hpp
	$(CXX) $(CXXFLAGS) -o $(TARGET) main.cpp amts.cpp GraphClass.cpp

.PHONY:  clean
clean:
	rm -r *.out *.o