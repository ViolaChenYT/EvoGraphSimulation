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
        if (arr[mid] < x && arr[mid+1]>=x)
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
	int *degrees, **edgelist;
	int counts[2] = { 0, 0 };
	double times[2] = { 0, 0 };
	double rt;
    ofstream file;
	mt19937 generator;
    void print_fit(double*);
    double sum_over_arr(double*);

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


Simulator::Simulator(string input_name, string output_name) {
    ifstream input(input_name);
    file.open(output_name);
    
    vector<int> out, in;
    int node;
    int i = 0;
    popsize = 0;
    while (input >> node)
    {
        popsize = (popsize < node) ? node: popsize;
        if (i % 2 == 0)
            out.push_back(node);
        else
            in.push_back(node);
        ++i;
    }
    if (out.size() != in.size())
        throw invalid_argument("in and out should have same length");
    ++popsize;
    // cout << popsize << endl;
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
        printf("%.3f ", fitness[i]);
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

void Simulator::simulate(double s = 0)
{
    this->s = s;
    uniform_real_distribution<double> rand(0.0, 1.0);
    uniform_real_distribution<double> randsmall(-0.05, 0.05);
    
    int populations[] = { popsize - 1, 1 };
    
    int *ntoi = new int[popsize];
    int *iton = new int[popsize];
    int *mutant = new int[popsize];
    double *fitness = new double[popsize];
    double *acc_fit = new double[popsize];
    // print_fit(fitness);
    for (int i = 0; i < popsize; ++i)
    {
        ntoi[i] = i;
        iton[i] = i;
        mutant[i] = 0;
        fitness[i] = 1;
    }
    
    //int index2 = popsize - 1;
    int index2 = (int)(rand(generator) * popsize);
    if (index2 == popsize){
        printf("yikes\n");
    }
    
    mutant[iton[index2]] = 1;
    fitness[iton[index2]] = 1 + s + randsmall(generator);
    permute(iton, ntoi, populations[0], index2);
    int t = 0;
    // population[0]: no. of WT, pop[1]: no. of mut
    while (populations[0] != 0 && populations[1] != 0)
    {
        ++t;
        
        double bar = populations[0]; // default fitness = 1
        double acc = 0;
        // calculate accummulated fitness
        for (int i = 0;i<popsize;i++){
            acc = acc + fitness[i];
            acc_fit[i] = acc;
        }
        double totalFitness = acc_fit[popsize-1];
        double birth = totalFitness * rand(generator);
        int birthIndex, birthNode, deathIndex, deathNode;
        // bin search to find birth node
        birthNode = binsearch(acc_fit,0,popsize-1,birth);
        if (birthNode == -1){
            printf("f\n");
            print_fit(acc_fit);
        }
        birthIndex = ntoi[birthNode];
        // printf("%d,%d,%d,%d\n",birthIndex,birthNode,deathIndex,deathNode);
        deathIndex = (int)(degrees[birthNode] * rand(generator));
        int* edges = edgelist[birthNode];
        deathNode = edges[deathIndex];
        // printf("just to confirm\n");
        if (mutant[deathNode] == mutant[birthNode]){
            if (mutant[birthNode]==1)
                fitness[deathNode] = 1 + randsmall(generator);
        }
        // printf("got here\n");
        if (mutant[deathNode] == 1)
        {
            --populations[1];
            index2 = populations[0];
            if (index2 == popsize){
                printf("rip\n");
            }
            permute(iton, ntoi, ntoi[deathNode], index2);
        }
        else
        {
            --populations[0];
            index2 = (popsize - 1) - populations[1];
            if (index2 < 0){
                printf("big rip\n");
            }
            fitness[deathNode] = 1 + s + randsmall(generator);
            permute(iton, ntoi, ntoi[deathNode], index2);
            //permute(fitness, ntoi[deathNode], index2);
        }
        
        if (mutant[birthNode] == 1)
            ++populations[1];
        else
            ++populations[0];
        
        mutant[deathNode] = mutant[birthNode];
        fitness[deathNode] = fitness[birthNode];
        //printf("end of loops\n");
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
    delete[] ntoi;
    delete[] iton;
}
// simulate birth-death processes for input trial number of times
void Simulator::simulate(int trials, double s = 0.0)
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
        simulate(s);
    }
    
    times[0] /= counts[0];
    times[1] /= counts[1];
    this->rt = static_cast<double>(clock() - start) / CLOCKS_PER_SEC;
    cout << rt << endl;
}

// simulates 1 death-birth process on network
void Simulator::simulate_dB(double s = 0)
{
    this->s = s;
    uniform_real_distribution<double> rand(0.0, 1.0);
    uniform_real_distribution<double> randsmall(-0.05, 0.05);
    
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
    printf("prob. ext = %.3f, prob. fix = %.3f,\n times: \t%f,\t%f\n", counts[0]/total, counts[1]/total, times[0], times[1]);
}

// save results of the simulations to output file stream
void Simulator::save()
{
    file << s << "\t";
    file << counts[0] << "\t";
    file << counts[1] << "\t";
    file << times[0] << "\t";
    file << times[1] << "\t";
    file << rt << endl;
}
