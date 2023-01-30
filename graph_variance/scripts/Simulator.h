//  Evograph
//
//  Modified by Viola Chen April 2022
//  Created by Yang Ping Kuo on 5/22/19.
//  Copyright © 2019 Yang Ping Kuo. All rights reserved.
//

#include <random>
#include <ctime>

#include <iostream>
#include <fstream>
#include <string>

#include <vector>
#include <stdexcept>

using namespace std;

int binsearch(double arr[], int lo, int hi, double x)
// search for the smallest value in arr that's greater than x and return its idx
{   if (arr[0] >= x)
        return 0;
    if (hi >= lo) {
        int mid = lo + (hi - lo) / 2;
        // If the element is present at the middle
        // itself
        if (arr[mid] >= x && arr[mid-1]<x)
            return mid;

        // If element is smaller than mid, then
        // it can only be present in left subarray
        if (arr[mid] >= x)
            return binsearch(arr, lo, mid - 1, x);

        // Else the element can only be present
        // in right subarray
        return binsearch(arr, mid + 1, hi, x);
    }
    return -1;
}

void permute(int *iton, int *ntoi, int index1, int index2){   
    int node1 = iton[index1];
    int node2 = iton[index2];
    
    iton[index1] = node2;
    iton[index2] = node1;
    
    ntoi[node1] = index2;
    ntoi[node2] = index1;
}

void permute(double* fitness, int index1, int index2){
    double node1 = fitness[index1];
    double node2 = fitness[index2];
    
    fitness[index1] = node2;
    fitness[index2] = node1;
}

class Simulator {
private:
	int popsize;
	double s;
    double var;
	int *degrees, **edgelist;
	int counts[2] = { 0, 0 };
	double times[2] = { 0, 0 };
	double rt;
    ofstream file;
	mt19937 generator;
    void print_fit(double*);
    double sum_over_arr(double*);

public:
    double fit;
	Simulator(string, string,double);
    ~Simulator();
    void simulate(double,double,string,int);
    void simulate(int, double,double, string);
    void simulate_dB(double);
    void simulate_dB(int, double);
    void print();
    void save();
};


Simulator::Simulator(string input_name, string output_name, double fit) {
    this->fit = fit;
    ifstream input(input_name);
    file.open(output_name);
    
    vector<int> out, in;
    int node1,node2;
    int i = 0;
    popsize = 0;
    while (input >> node1 >> node2)
    {
        popsize = (popsize < node1) ? node1: popsize;
        popsize = (popsize < node2) ? node2: popsize;
        out.push_back(node1);
        in.push_back(node2);
        ++i;
    }
    if (out.size() != in.size())
        throw invalid_argument("in and out should have same length");
    ++popsize;
    generator = mt19937((unsigned int)time(NULL));
    
    degrees = new int[popsize];
    int *temp = new int[popsize];
    
    for (int node = 0; node < popsize; ++node) {
        temp[node] = 0;
        degrees[node] = 0;
    }
    
    for (auto node : out)
        ++degrees[node];
    
    for (auto node : in)
        ++degrees[node];
    
    edgelist = new int*[popsize];
    for (int node = 0; node < popsize; ++node) {
        edgelist[node] = new int[degrees[node]];
    }
    
    for (int i = 0; i < in.size(); ++i) {
        int node1 = in[i];
        int node2 = out[i];
        edgelist[node1][temp[node1]] = node2;
        edgelist[node2][temp[node2]] = node1;
        ++temp[node1];
        ++temp[node2];
    }
    delete[] temp;
}

Simulator::~Simulator()
{
    for (int node = 0; node < popsize; ++node) {
        delete [] edgelist[node];
    }
    delete [] edgelist;
    delete [] degrees;

    file.close();
}

void Simulator::print_fit(double* fitness){
    for (int i = 0; i < popsize;i++){
        if (fitness[i] > 1)
            printf("%.2f\t", fitness[i]);
    }
    cout << endl;
}

double Simulator::sum_over_arr(double* fitness){
    double ans = 0;
    for (int i = 0; i < popsize;i++){
        ans = ans + fitness[i];
    }
    return ans;
}

void Simulator::simulate(double s = 0, double var = 0, string dist = "uniform", int iter=0)
{
    this->s = s;
    this->var = var;
    uniform_real_distribution<double> rand(0.0, 1.0);
    uniform_real_distribution<double> randsmall(-var, var);
    poisson_distribution<int> poi(fit);
    bernoulli_distribution rolldie(0.5);

    int populations[] = { popsize - 1, 1, 0 }; // no. of WT / good mutant / bad mutant
    // if no bad mutant, population[1] refers to number of mutants in general
    int *mutant = new int[popsize]; // 0: WT, -1: neg mutant, 1: pos mutant
    double *fitness = new double[popsize]; 
    // fitness and acc_fitness index follows mutant idx, and same as b/dNode
    double *acc_fit = new double[popsize];
    // 
    for (int i = 0; i < popsize; ++i)
    {
        mutant[i] = 0;
        fitness[i] = fit;
    }
    
    //int index2 = popsize - 1;
    int index2 = (int)(rand(generator) * popsize);
    // setting initial to be good mutant for now
    mutant[index2] = 1;
    // it can be bad -> -1
    if (dist == "poisson")
        fitness[index2] =  poi(generator);
    else if (dist == "uniform")
        fitness[index2] = fit + s + randsmall(generator);
    else if (dist == "binom"){
        double offset;
        if (mutant[index2] > 0){
            offset = var;
        } else {
            offset = -var;
        }
        // if (rolldie(generator)){
        //     offset = var;
        // } else{
        //     offset = -var;
        // }
        fitness[index2] = fit + s + offset; 
    }
    else if (dist == "left"){
        double offset;
        double u = rand(generator);
        if (u < 0.5){
            offset = -0.5;
        } else if (u > 0.75) {
            offset = 1;
        } else {
            offset = 0;
        }
        fitness[index2] = fit + s + offset;
    } 
    else if (dist == "mid"){
        double offset;
        if (rolldie(generator)){
            offset = 0.5;
        } else{
            offset = -0.5;
        }
        fitness[index2] = fit + s + offset; 
    }
    else if (dist == "right"){
        double offset;
        double u = rand(generator);
        if (u < 0.25){
            offset = -1;
        } else if (u > 0.5) {
            offset = 0.5;
        } else {
            offset = 0;
        }
        fitness[index2] = fit + s + offset;
    }
    int t = 0;
    // population[0]: no. of WT, pop[1]: no. of mut
    while (populations[0] != 0 && (populations[1]+populations[2]) != 0){
        if (t % 50 == 0) {
            printf("%d\t%d\t%d\n", populations[0],populations[1],populations[2]);
        }
        ++t;
        double acc = 0;
        // print_fit(fitness);
        // calculate accummulated fitness
        for (int i = 0;i<popsize;i++){
            acc = acc + fitness[i];
            acc_fit[i] = acc;
        }
        double totalFitness = acc;
        double birth = totalFitness * rand(generator);
        int birthIndex, birthNode, deathIndex, deathNode;
        // bin search to find birth node
        birthNode = binsearch(acc_fit,0,popsize-1,birth);
        //printf("birthnode, %d -- %.2f\n", birthNode, birth);
        if (birthNode == -1){
            printf("f\n");
            print_fit(acc_fit);
        }
        deathIndex = (int)(degrees[birthNode] * rand(generator));
        int* edges = edgelist[birthNode];
        deathNode = edges[deathIndex];
        //printf("birth: %d, death: %d\n", birthNode, deathNode);
        if (abs(mutant[deathNode]) == abs(mutant[birthNode])){
            continue;
        }
        if (abs(mutant[deathNode]) == 1){
            if (mutant[deathNode] > 0){
                --populations[1];
            } else {
                --populations[2];
            }
            ++populations[0];
            fitness[deathNode] = fit;
            mutant[deathNode] = 0;
        }
        else {
            --populations[0];
            if (dist == "poisson")
                fitness[deathNode] =  poi(generator);
            else if (dist == "uniform")
                fitness[deathNode] = fit + s + randsmall(generator);
            else if (dist == "binom"){
                double offset;
                if (rolldie(generator)){
                    offset = var;
                    mutant[deathNode] = 1;
                    ++populations[1];
                } else{
                    offset = -var;
                    mutant[deathNode] = -1;
                    ++populations[2];
                }
                fitness[deathNode] = fit + s + offset; 
            }
             else if (dist == "left"){
                double offset;
                double u = rand(generator);
                if (u < 0.5){
                    offset = -0.5;
                } else if (u > 0.75) {
                    offset = 1;
                } else {
                    offset = 0;
                }
                fitness[index2] = fit + s + offset;
            } 
            else if (dist == "mid"){
                double offset;
                if (rolldie(generator)){
                    offset = 0.5;
                } else{
                    offset = -0.5;
                }
                fitness[index2] = fit + s + offset; 
            }
            else if (dist == "right"){
                double offset;
                double u = rand(generator);
                if (u < 0.25){
                    offset = -1;
                } else if (u > 0.5) {
                    offset = 0.5;
                } else {
                    offset = 0;
                }
                fitness[index2] = fit + s + offset;
            }
        }
    }
    
    if (populations[0] == 0)
    {
        ++counts[1];
        times[1] += t;
    }
    else
    {
        ++counts[0];
        times[0] += t;
    }
    delete populations;
    delete[] mutant;
    delete[] fitness;
    delete[] acc_fit;
}
// simulate birth-death processes for input trial number of times
void Simulator::simulate(int trials, double s = 0.0, double var = 0, string dist = "uniform")
{
    generator = mt19937((unsigned int)time(NULL));
    clock_t start = clock();
    // Parallelized using openMP to create threads
    counts[0] = 0;
    counts[1] = 0;
    times[0] = 0;
    times[1] = 0;
    cout << dist << "\t";
    file << dist << "\t";
    file << fit << "\t";
    cout << fit << "\t";
    file << var << "\t";
    cout << var << "\t";
    file << s << "\t";
    cout << s << "\t";
    for (int i = 0; i < trials; ++i)
    {
        if (i % 20 == 0) {
            // cout << "." << flush;
        }
        simulate(s,var,dist,i);
    }
    
    times[0] /= counts[0];
    times[1] /= counts[1];
    this->rt = static_cast<double>(clock() - start) / CLOCKS_PER_SEC;
    // cout << rt << endl;
}

// simulates 1 death-birth process on network
void Simulator::simulate_dB(double s = 0)
{
    this->s = s;
    uniform_real_distribution<double> rand(0.0, 1.0);
    
    double fitness[] = { 1.0, 1.0 + s };
    int populations[] = { popsize - 1, 1 };
    
    double *localFitness = new double[popsize];
    int *mutant = new int[popsize];
    
    for (int i = 0; i < popsize; ++i)
    {
        localFitness[i] = degrees[i];
        mutant[i] = 0;
    }
    
    int node, deathnode;
    int birthnode = (int)(rand(generator) * popsize);
    
    mutant[birthnode] = 1;
    
    for (int d = 0; d < degrees[birthnode]; ++d)
    {
        node = edgelist[birthnode][d];
        localFitness[node] += s;
    }
    
    int t = 0;
    while (populations[0] != 0 && populations[1] != 0) // what does this mean?
    {
        ++t;
        deathnode = (int)(rand(generator) * popsize);
        double draw = rand(generator) * localFitness[deathnode];
        
        for (int d = 0; d < degrees[deathnode]; ++d)
        {
            node = edgelist[deathnode][d];
            draw -= (1 + s * mutant[node]);
            
            if (draw <= 0)
            {
                birthnode = node;
                break;
            }
            else if (d + 1 == degrees[deathnode])
                birthnode = node;
        }
        
        if (mutant[deathnode] == 1)
        {
            --populations[1];
            for (int d = 0; d < degrees[deathnode]; ++d)
            {
                node = edgelist[deathnode][d];
                localFitness[node] -= s;
            }
        }
        else
            --populations[0];
        
        if (mutant[birthnode] == 1)
        {
            ++populations[1];
            for (int d = 0; d < degrees[deathnode]; ++d)
            {
                node = edgelist[deathnode][d];
                localFitness[node] += s;
            }
        }
        else
            ++populations[0];
        mutant[deathnode] = mutant[birthnode];
    }
    
    if (populations[0] == 0)
    {
        ++counts[1];
        times[1] += t;
    }
    else
    {
        ++counts[0];
        times[0] += t;
    }
    delete[] mutant;
    delete[] localFitness;
}

void Simulator::simulate_dB(int trials, double s = 0.0)
{
    generator = mt19937((unsigned int)time(NULL));
    clock_t start = clock();
    // Parallelized using openMP to create threads
    counts[0] = 0;
    counts[1] = 0;
    times[0] = 0;
    times[1] = 0;
    
    for (int i = 0; i < trials; ++i)
    {
        //cout << "run " << i << endl;
        simulate_dB(s);
    }
    
    times[0] /= counts[0];
    times[1] /= counts[1];
    this->rt = static_cast<double>(clock() - start) / CLOCKS_PER_SEC;
    cout << rt << endl;
}

void Simulator::print(){
    double total = counts[0] + counts[1];
    printf("%.5f\n", counts[1]/total);
}

// save results of the simulations to output file stream
void Simulator::save()
{
    double total = counts[0] + counts[1];
    file << counts[1]/total << endl;
    cout << counts[1]/total << endl;
    /* file << s << "\t";
    file << var << "\t";
    file << counts[0] << "\t";
    file << counts[1] << "\t";
    file << times[0] << "\t";
    file << times[1] << "\t"; */
}
