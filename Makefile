CXX = g++
CXXFLAGS = -std=c++17 -O2 -Wall
TARGET = war_simulator
SRCS = new_cpp/war_simulator.cpp

all: $(TARGET)

$(TARGET): $(SRCS)
	$(CXX) $(CXXFLAGS) -o $@ $^

clean:
	rm -f $(TARGET)

.PHONY: all clean
