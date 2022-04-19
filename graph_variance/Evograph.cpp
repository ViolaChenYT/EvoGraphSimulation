//  Evograph
//
//  Created by Yang Ping Kuo on 5/22/19.
//  Copyright © 2019 Yang Ping Kuo. All rights reserved.
//
#pragma once

#include <iostream>
#include "Simulator.h"
#include <random>
#include <fstream>
#include <string>

using namespace std;

int main(int argc, char **argv)
{
    if (argc < 5) {
        cout << "input format: graph_file | output_filename | num_runs | fitness(float) | alternative fitness ..." << endl;
        exit(1);
    }
    
    string input = argv[1];
    Simulator sim(argv[1], argv[2]);
    
    int runs = atoi(argv[3]);
    
    for(int i = 4; i < argc; ++i) {
        double fitness = atof(argv[i]);
        printf("fitness: %f\n",fitness );
        
        sim.simulate(runs, fitness);
        sim.print();
        sim.save();
    }
    
    /* for(int i = 4; i < argc; ++i) {
        double fitness = atof(argv[i]);
        cout << fitness << endl;
        
        sim.simulate_dB(runs, fitness);
        sim.print();
        sim.save();
    } */
    
    
    return 1;
}
