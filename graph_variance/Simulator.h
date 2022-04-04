//  Evograph
//
//  Created by Yang Ping Kuo on 5/22/19.
//  Copyright © 2019 Yang Ping Kuo. All rights reserved.
//

#pragma once

#include <random>
#include <ctime>

#include <iostream>
#include <fstream>
#include <string>

#include <vector>
#include <stdexcept>

using namespace std;

class Simulator {
private:
	int popsize;
	double s;
	int *degrees, **edgelist;
	int counts[2] = { 0, 0 };
	double times[2] = { 0, 0 };
	double rt;
    ofstream file;
	mt19937 generator;

public:
	Simulator(string, string);
    ~Simulator();
    void simulate(double);
    void simulate(int, double);
    void simulate_dB(double);
    void simulate_dB(int, double);
    void print();
    void save();
};