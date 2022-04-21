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
    if (argc < 6) {
        //cout << "input format: graph_file | output_filename | num_runs | base fitness | fitness(float) | var in fitness" << endl;
        exit(1);
    }
    
    string input = argv[1];
    
    int runs = atoi(argv[3]);
    string dist = argv[4];
    double fit = atof(argv[5]);
    Simulator sim(argv[1], argv[2],fit);
    double s = atof(argv[6]);
    double var = atof(argv[7]);
    cout << dist << "\t";
    printf("%f\t%f\t%f\t",fit,var,s);
    
    sim.simulate(runs, s, var, dist = dist);
    sim.print();
    //sim.save();
    
    
    /* for(int i = 4; i < argc; ++i) {
        double fitness = atof(argv[i]);
        cout << fitness << endl;
        
        sim.simulate_dB(runs, fitness);
        sim.print();
        sim.save();
    } */
    return 1;
}
